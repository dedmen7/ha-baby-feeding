"""Feeding rhythm: three hours by day and the night interval for bottles started at night."""

from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from zoneinfo import ZoneInfo

DAY_INTERVAL_HOURS = 3
DEFAULT_NIGHT_INTERVAL_HOURS = 4
MINIMUM_NIGHT_INTERVAL_HOURS = 3
MAXIMUM_NIGHT_INTERVAL_HOURS = 8
NIGHT_STARTS_AT = time(hour=22, minute=30)
NIGHT_ENDS_AT = time(hour=7)


@dataclass(frozen=True)
class NightRhythm:
    """The parents' choice for nights: the default four hours or their own interval."""

    custom_enabled: bool = False
    custom_hours: int = DEFAULT_NIGHT_INTERVAL_HOURS

    def __post_init__(self) -> None:
        whole_hours = isinstance(self.custom_hours, int) and not isinstance(self.custom_hours, bool)
        if not whole_hours or not MINIMUM_NIGHT_INTERVAL_HOURS <= self.custom_hours <= MAXIMUM_NIGHT_INTERVAL_HOURS:
            raise ValueError('Choose a night interval of 3 to 8 whole hours.')

    @property
    def interval_hours(self) -> int:
        return self.custom_hours if self.custom_enabled else DEFAULT_NIGHT_INTERVAL_HOURS


def started_at_night(*, start: datetime, time_zone: ZoneInfo) -> bool:
    local_time = _aware(start).astimezone(time_zone).time()
    return local_time >= NIGHT_STARTS_AT or local_time < NIGHT_ENDS_AT


def interval_hours(*, start: datetime, night_rhythm: NightRhythm, time_zone: ZoneInfo) -> int:
    at_night = started_at_night(start=start, time_zone=time_zone)
    return night_rhythm.interval_hours if at_night else DAY_INTERVAL_HOURS


def next_due(*, start: datetime, night_rhythm: NightRhythm, time_zone: ZoneInfo) -> datetime:
    hours = interval_hours(start=start, night_rhythm=night_rhythm, time_zone=time_zone)
    # Adding in UTC counts elapsed hours across a daylight-saving change.
    return _aware(start).astimezone(UTC) + timedelta(hours=hours)


def _aware(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        raise ValueError('A feeding moment needs a time zone.')
    return moment
