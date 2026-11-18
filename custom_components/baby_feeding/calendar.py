"""The feeding diary as a read-only calendar, so the history stays visible in Home Assistant's calendar."""

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from . import BabyFeedingConfigEntry
from .diary import Feed
from .manager import FeedingManager

EVENT_LENGTH = timedelta(minutes=1)


async def async_setup_entry(hass: HomeAssistant, entry: BabyFeedingConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    async_add_entities([FeedingDiaryCalendar(entry.runtime_data)])


class FeedingDiaryCalendar(CalendarEntity):
    _attr_should_poll = False
    _attr_name = 'Voedingsdagboek'
    _attr_unique_id = 'baby_feeding_diary'
    _attr_icon = 'mdi:notebook-outline'

    def __init__(self, manager: FeedingManager) -> None:
        self.manager = manager

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.manager.async_add_listener(self.async_write_ha_state))

    @property
    def event(self) -> CalendarEvent | None:
        feeds = self.manager.state.feeds
        return _event(feeds[-1]) if feeds else None

    async def async_get_events(self, hass: HomeAssistant, start_date: datetime, end_date: datetime) -> list[CalendarEvent]:
        return [_event(feed) for feed in self.manager.state.feeds if feed.start < end_date and feed.start + EVENT_LENGTH > start_date]


def _event(feed: Feed) -> CalendarEvent:
    start = dt_util.as_local(feed.start)
    return CalendarEvent(start=start, end=start + EVENT_LENGTH, summary=str(feed.amount) + ' cc', uid=feed.feed_id)
