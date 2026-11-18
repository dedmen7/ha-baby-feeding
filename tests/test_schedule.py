"""Feeding rhythm: three hours by day, the night interval for bottles started at night, in elapsed hours."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from custom_components.baby_feeding.schedule import NightRhythm, interval_hours, next_due

AMSTERDAM = ZoneInfo('Europe/Amsterdam')

DEFAULT_NIGHT_CASES = [
    ('2026-11-14T11:00:00+01:00', 3, '2026-11-14T14:00:00+01:00'),
    ('2026-11-14T22:29:00+01:00', 3, '2026-11-15T01:29:00+01:00'),
    ('2026-11-14T22:29:59+01:00', 3, '2026-11-15T01:29:59+01:00'),
    ('2026-11-14T22:30:00+01:00', 4, '2026-11-15T02:30:00+01:00'),
    ('2026-11-14T22:45:00+01:00', 4, '2026-11-15T02:45:00+01:00'),
    ('2026-11-14T23:00:00+01:00', 4, '2026-11-15T03:00:00+01:00'),
    ('2026-11-15T03:00:00+01:00', 4, '2026-11-15T07:00:00+01:00'),
    ('2026-11-15T06:59:59+01:00', 4, '2026-11-15T10:59:59+01:00'),
    ('2026-11-15T07:00:00+01:00', 3, '2026-11-15T10:00:00+01:00'),
    ('2026-03-28T23:00:00+01:00', 4, '2026-03-29T04:00:00+02:00'),
    ('2026-10-24T23:00:00+02:00', 4, '2026-10-25T02:00:00+01:00'),
    ('2026-10-25T02:38:47+02:00', 4, '2026-10-25T05:38:47+01:00'),
    ('2026-10-25T02:38:47+01:00', 4, '2026-10-25T06:38:47+01:00'),
]

FIVE_HOUR_NIGHT_CASES = [
    ('2026-11-14T22:29:59+01:00', 3, '2026-11-15T01:29:59+01:00'),
    ('2026-11-14T22:30:00+01:00', 5, '2026-11-15T03:30:00+01:00'),
    ('2026-11-14T23:00:00+01:00', 5, '2026-11-15T04:00:00+01:00'),
    ('2026-11-15T06:59:59+01:00', 5, '2026-11-15T11:59:59+01:00'),
    ('2026-11-15T07:00:00+01:00', 3, '2026-11-15T10:00:00+01:00'),
    ('2026-03-28T23:00:00+01:00', 5, '2026-03-29T05:00:00+02:00'),
    ('2026-10-24T23:00:00+02:00', 5, '2026-10-25T03:00:00+01:00'),
    ('2026-10-25T02:38:47+02:00', 5, '2026-10-25T06:38:47+01:00'),
    ('2026-10-25T02:38:47+01:00', 5, '2026-10-25T07:38:47+01:00'),
]


def moment(value: str) -> datetime:
    return datetime.fromisoformat(value)


def assert_rhythm(*, night_rhythm: NightRhythm, given: str, hours: int, expected: str) -> None:
    start = moment(given)
    assert interval_hours(start=start, night_rhythm=night_rhythm, time_zone=AMSTERDAM) == hours
    due = next_due(start=start, night_rhythm=night_rhythm, time_zone=AMSTERDAM)
    assert due == moment(expected)
    assert due - start == timedelta(hours=hours)


@pytest.mark.parametrize(('given', 'hours', 'expected'), DEFAULT_NIGHT_CASES)
def test_default_rhythm_counts_three_hours_by_day_and_four_at_night(given: str, hours: int, expected: str) -> None:
    assert_rhythm(night_rhythm=NightRhythm(), given=given, hours=hours, expected=expected)


@pytest.mark.parametrize(('given', 'hours', 'expected'), FIVE_HOUR_NIGHT_CASES)
def test_custom_night_interval_applies_between_half_past_ten_and_seven(given: str, hours: int, expected: str) -> None:
    assert_rhythm(night_rhythm=NightRhythm(custom_enabled=True, custom_hours=5), given=given, hours=hours, expected=expected)


@pytest.mark.parametrize(('given', 'hours'), [('22:29', 3), ('22:30', 4), ('23:00', 4), ('06:59', 4), ('07:00', 3)])
def test_disabled_custom_interval_keeps_four_hour_nights_and_remembers_the_choice(given: str, hours: int) -> None:
    night_rhythm = NightRhythm(custom_enabled=False, custom_hours=5)
    start = moment('2026-11-14T' + given + ':00+01:00')
    assert interval_hours(start=start, night_rhythm=night_rhythm, time_zone=AMSTERDAM) == hours
    assert night_rhythm.custom_hours == 5


@pytest.mark.parametrize('hours', [3, 4, 5, 6, 7, 8])
def test_night_interval_accepts_whole_hours_from_three_to_eight(hours: int) -> None:
    assert NightRhythm(custom_enabled=True, custom_hours=hours).interval_hours == hours


@pytest.mark.parametrize('hours', [2, 9, -1, 5.5, '5', None, True, float('nan'), float('inf')])
def test_night_interval_rejects_anything_else(hours: object) -> None:
    with pytest.raises(ValueError):
        NightRhythm(custom_enabled=True, custom_hours=hours)


def test_interval_is_elapsed_time_for_a_start_in_the_local_zone() -> None:
    start = datetime(year=2026, month=3, day=28, hour=23, tzinfo=AMSTERDAM)
    due = next_due(start=start, night_rhythm=NightRhythm(), time_zone=AMSTERDAM)
    assert due == moment('2026-03-29T04:00:00+02:00')
    assert due.astimezone(AMSTERDAM).hour == 4


def test_a_start_without_time_zone_is_refused() -> None:
    with pytest.raises(ValueError):
        next_due(start=datetime(year=2026, month=11, day=14, hour=11), night_rhythm=NightRhythm(), time_zone=AMSTERDAM)
