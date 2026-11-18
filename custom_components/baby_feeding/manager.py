"""Runs the diary inside Home Assistant: stores changes, times the reminder and keeps the phones up to date."""

import asyncio
import logging
import re
import uuid
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers.event import async_call_later, async_track_point_in_time, async_track_time_interval
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from . import diary
from .const import (
    CONF_DASHBOARD_URL,
    CONF_NOTIFY_SERVICES,
    DEFAULT_DASHBOARD_URL,
    DOMAIN,
    PHONE_UPDATE_DELAY_SECONDS,
    STORAGE_KEY,
    STORAGE_VERSION,
    WIDGET_REFRESH,
)
from .diary import Feed, FeedError, FeedingState
from .display import lock_screen_message, next_bottle_text
from .persistence import from_stored, to_stored
from .planning import plan_for_feed
from .schedule import NightRhythm
from .texts import text

_LOGGER = logging.getLogger(__name__)
IMPORTED_AMOUNT = re.compile(r'^\s*(\d+)\s*(cc|ml)\s*$', re.IGNORECASE)


class FeedingManager:
    """Owns the diary state; every change goes through `_change` so storage, timers and phones stay in step."""

    def __init__(self, hass: HomeAssistant, *, notify_services: list[str], dashboard_url: str) -> None:
        self.hass = hass
        self.notify_services = notify_services
        self.dashboard_url = dashboard_url or DEFAULT_DASHBOARD_URL
        self.state = FeedingState()
        self._store: Store[dict[str, Any]] = Store(hass=hass, version=STORAGE_VERSION, key=STORAGE_KEY)
        self._lock = asyncio.Lock()
        self._listeners: list[Callable[[], None]] = []
        self._unsubscribers: list[CALLBACK_TYPE] = []
        self._due_timer: CALLBACK_TYPE | None = None
        self._phone_timer: CALLBACK_TYPE | None = None
        self._sent_countdown: tuple | None = None
        self._sent_widget_text: str | None = None

    @classmethod
    def from_entry_data(cls, hass: HomeAssistant, data: dict[str, Any]) -> 'FeedingManager':
        return cls(hass, notify_services=list(data.get(CONF_NOTIFY_SERVICES, [])), dashboard_url=data.get(CONF_DASHBOARD_URL, DEFAULT_DASHBOARD_URL))

    @property
    def time_zone(self) -> ZoneInfo:
        return ZoneInfo(self.hass.config.time_zone)

    @property
    def language(self) -> str:
        return self.hass.config.language

    async def async_start(self) -> None:
        stored = await self._store.async_load()
        if stored is not None:
            self.state = from_stored(stored)
        self._sent_widget_text = next_bottle_text(plan=self.state.plan, now=dt_util.now(), time_zone=self.time_zone, language=self.language)
        self._unsubscribers.append(async_track_time_interval(hass=self.hass, action=self._async_minute, interval=timedelta(minutes=1)))
        self._schedule_due()
        await self._async_handle_due()

    @callback
    def async_stop(self) -> None:
        for unsubscribe in (*self._unsubscribers, self._due_timer, self._phone_timer):
            if unsubscribe is not None:
                unsubscribe()
        self._unsubscribers.clear()
        self._due_timer = self._phone_timer = None

    @callback
    def async_add_listener(self, listener: Callable[[], None]) -> CALLBACK_TYPE:
        self._listeners.append(listener)
        return lambda: self._listeners.remove(listener)

    async def async_save_bottle(self, *, start: datetime, amount: int) -> FeedingState:
        now = dt_util.now()
        return await self._change(lambda state: diary.save_bottle(state, start=start, amount=amount, now=now, time_zone=self.time_zone, new_id=_new_id))

    async def async_add_earlier_feed(self, *, start: datetime, amount: int) -> FeedingState:
        now = dt_util.now()
        return await self._change(lambda state: diary.add_earlier_feed(state, start=start, amount=amount, now=now, new_id=_new_id))

    async def async_update_feed(self, *, feed_id: str, start: datetime, amount: int) -> FeedingState:
        now = dt_util.now()
        return await self._change(lambda state: diary.update_feed(state, feed_id=feed_id, start=start, amount=amount, now=now, time_zone=self.time_zone))

    async def async_delete_feed(self, *, feed_id: str) -> FeedingState:
        now = dt_util.now()
        return await self._change(lambda state: diary.delete_feed(state, feed_id=feed_id, now=now, time_zone=self.time_zone))

    async def async_new_bottle(self) -> FeedingState:
        now = dt_util.now()
        return await self._change(lambda state: diary.open_new_bottle(state, now=now))

    async def async_set_settings(self, *, standard_amount: int, maximum_amount: int | None, night_custom_enabled: bool, night_hours: int) -> FeedingState:
        now = dt_util.now()

        def change(state: FeedingState) -> FeedingState:
            try:
                rhythm = NightRhythm(custom_enabled=night_custom_enabled, custom_hours=night_hours)
            except ValueError as error:
                raise FeedError('invalid_night_interval') from error
            with_amounts = diary.set_amounts(state, standard_amount=standard_amount, maximum_amount=maximum_amount)
            return diary.set_night_rhythm(with_amounts, night_rhythm=rhythm, now=now, time_zone=self.time_zone)

        return await self._change(change)

    async def async_import_calendar(self, *, entity_id: str) -> dict[str, int]:
        if self.state.feeds:
            raise FeedError('import_needs_empty_diary')
        now = dt_util.now()
        response = await self.hass.services.async_call(
            domain='calendar', service='get_events',
            service_data={'entity_id': entity_id, 'start_date_time': datetime(year=2000, month=1, day=1, tzinfo=self.time_zone), 'end_date_time': now + timedelta(days=2)},
            blocking=True, return_response=True,
        )
        events = (response or {}).get(entity_id, {}).get('events', [])
        feeds, skipped = _feeds_from_events(events)

        def change(state: FeedingState) -> FeedingState:
            imported = FeedingState(feeds=feeds, night_rhythm=state.night_rhythm, standard_amount=state.standard_amount, maximum_amount=state.maximum_amount)
            newest = max((feed for feed in feeds if feed.start <= now + diary.AHEAD_LIMIT), key=lambda feed: feed.start, default=None)
            if newest is None:
                return imported
            plan = plan_for_feed(feed_id=newest.feed_id, feed_start=newest.start, night_rhythm=state.night_rhythm, time_zone=self.time_zone)
            # A moment that already passed before the import was handled by the old setup and must not alert again.
            passed = plan.due <= now
            return replace(imported, plan=replace(plan, alerted=passed, claimed=passed))

        await self._change(change)
        return {'imported': len(feeds), 'skipped': skipped}

    async def _change(self, change: Callable[[FeedingState], FeedingState]) -> FeedingState:
        async with self._lock:
            try:
                updated = change(self.state)
            except FeedError as error:
                raise ServiceValidationError(str(error), translation_domain=DOMAIN, translation_key=error.key) from error
            if updated == self.state:
                return updated
            self.state = updated
            await self._store.async_save(to_stored(updated))
        self._after_change()
        await self._async_handle_due()
        return updated

    @callback
    def _after_change(self) -> None:
        self._schedule_due()
        self._schedule_phone_update()
        self._notify_listeners()

    @callback
    def _notify_listeners(self) -> None:
        for listener in list(self._listeners):
            listener()

    @callback
    def _schedule_due(self) -> None:
        if self._due_timer is not None:
            self._due_timer()
            self._due_timer = None
        plan = self.state.plan
        if plan is not None and plan.due > dt_util.now():
            self._due_timer = async_track_point_in_time(hass=self.hass, action=self._async_due_reached, point_in_time=plan.due)

    async def _async_due_reached(self, _moment: datetime) -> None:
        self._due_timer = None
        await self._async_handle_due()
        self._schedule_phone_update()
        self._notify_listeners()

    async def _async_handle_due(self) -> None:
        now = dt_util.now()
        async with self._lock:
            updated, alerted = diary.alert(self.state, now=now)
            if not alerted:
                return
            self.state = updated
            await self._store.async_save(to_stored(updated))
        self._notify_listeners()
        self._schedule_phone_update()
        reminder = {'title': text(self.language, 'reminder_title'), 'message': text(self.language, 'reminder_message'), 'data': {'url': self.dashboard_url, 'push': {'sound': {'name': 'default', 'critical': 1, 'volume': 1.0}}}}
        await self._async_send_to_phones(reminder)

    @callback
    def _async_minute(self, _moment: datetime) -> None:
        self._notify_listeners()

    @callback
    def _schedule_phone_update(self) -> None:
        if self._phone_timer is not None:
            self._phone_timer()
        self._phone_timer = async_call_later(hass=self.hass, delay=PHONE_UPDATE_DELAY_SECONDS, action=self._async_update_phones)

    async def _async_update_phones(self, _moment: datetime) -> None:
        self._phone_timer = None
        now = dt_util.now()
        plan = self.state.plan
        if plan is not None:
            countdown = (plan.feed_id, plan.feed_start, plan.due, plan.due <= now)
            message = lock_screen_message(plan=plan, now=now, time_zone=self.time_zone, dashboard_url=self.dashboard_url, language=self.language)
            if message is not None and countdown != self._sent_countdown:
                self._sent_countdown = countdown
                await self._async_send_to_phones(message)
        widget_text = next_bottle_text(plan=plan, now=now, time_zone=self.time_zone, language=self.language)
        if widget_text != self._sent_widget_text:
            self._sent_widget_text = widget_text
            await self._async_send_to_phones({'message': WIDGET_REFRESH})

    async def _async_send_to_phones(self, data: dict[str, Any]) -> None:
        for service in self.notify_services:
            domain, _, name = service.partition('.')
            try:
                await self.hass.services.async_call(domain=domain, service=name, service_data=data, blocking=True)
            except HomeAssistantError as error:
                _LOGGER.warning('Sending to %s failed: %s', service, error)


def _new_id() -> str:
    return uuid.uuid4().hex


def _feeds_from_events(events: list[dict[str, Any]]) -> tuple[tuple[Feed, ...], int]:
    feeds: list[Feed] = []
    taken: set[datetime] = set()
    skipped = 0
    for event in events:
        match = IMPORTED_AMOUNT.match(str(event.get('summary', '')))
        start = dt_util.parse_datetime(str(event.get('start', '')))
        if match is None or start is None or start.tzinfo is None or int(match.group(1)) > diary.MAXIMUM_AMOUNT:
            skipped += 1
            continue
        minute = start.replace(second=0, microsecond=0)
        if minute in taken:
            skipped += 1
            continue
        taken.add(minute)
        feeds.append(Feed(feed_id=_new_id(), start=start, amount=int(match.group(1))))
    return tuple(sorted(feeds, key=lambda feed: feed.start)), skipped
