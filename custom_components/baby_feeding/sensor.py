"""Sensors for widgets and the dashboard card: next bottle, progress and the full diary status."""

from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from . import BabyFeedingConfigEntry
from .display import next_bottle_text, progress_percent
from .manager import FeedingManager

STATUS_DAYS_BACK = 7


async def async_setup_entry(hass: HomeAssistant, entry: BabyFeedingConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    manager = entry.runtime_data
    async_add_entities([NextFeedingSensor(manager), NextBottleSensor(manager), ProgressSensor(manager), StatusSensor(manager)])


class FeedingSensor(SensorEntity):
    """Entity IDs are fixed in English so automations and widgets do not depend on the system language."""

    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(self, manager: FeedingManager, *, key: str, icon: str) -> None:
        self.manager = manager
        self.entity_id = 'sensor.baby_feeding_' + key
        self._attr_unique_id = 'baby_feeding_' + key
        self._attr_translation_key = key
        self._attr_icon = icon

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.manager.async_add_listener(self.async_write_ha_state))


class NextFeedingSensor(FeedingSensor):
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, manager: FeedingManager) -> None:
        super().__init__(manager, key='next_feeding', icon='mdi:baby-bottle-outline')

    @property
    def native_value(self) -> datetime | None:
        plan = self.manager.state.plan
        return None if plan is None else plan.due


class NextBottleSensor(FeedingSensor):
    """The next bottle as short text for phone widgets, in the Home Assistant language."""

    def __init__(self, manager: FeedingManager) -> None:
        super().__init__(manager, key='next_bottle', icon='mdi:baby-bottle-outline')

    @property
    def native_value(self) -> str:
        return next_bottle_text(plan=self.manager.state.plan, now=dt_util.now(), time_zone=self.manager.time_zone, language=self.manager.language)


class ProgressSensor(FeedingSensor):
    _attr_native_unit_of_measurement = '%'

    def __init__(self, manager: FeedingManager) -> None:
        super().__init__(manager, key='progress', icon='mdi:progress-clock')

    @property
    def native_value(self) -> int:
        return progress_percent(plan=self.manager.state.plan, now=dt_util.now())


class StatusSensor(FeedingSensor):
    """Everything the dashboard card needs; the large attributes stay out of the recorder."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ['open', 'saved']
    _unrecorded_attributes = frozenset({'plan', 'feeds', 'open_start'})

    def __init__(self, manager: FeedingManager) -> None:
        super().__init__(manager, key='status', icon='mdi:notebook-outline')

    @property
    def native_value(self) -> str:
        state = self.manager.state
        return 'open' if state.plan is None or state.pending is not None else 'saved'

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        state = self.manager.state
        plan = state.plan
        since = dt_util.start_of_local_day() - timedelta(days=STATUS_DAYS_BACK)
        return {
            'plan': None if plan is None else {
                'feed_id': plan.feed_id, 'feed_start': _local(plan.feed_start), 'due': _local(plan.due), 'alerted': plan.alerted,
            },
            'open_start': None if state.pending is None else _local(state.pending),
            'standard_amount': state.standard_amount,
            'maximum_amount': state.maximum_amount,
            'night_custom_enabled': state.night_rhythm.custom_enabled,
            'night_hours': state.night_rhythm.custom_hours,
            'night_starts_at': state.night_rhythm.starts_at.strftime('%H:%M'),
            'feeds': [{'id': feed.feed_id, 'start': _local(feed.start), 'amount': feed.amount} for feed in state.feeds if feed.start >= since],
        }


def _local(moment: datetime) -> str:
    return dt_util.as_local(moment).isoformat()
