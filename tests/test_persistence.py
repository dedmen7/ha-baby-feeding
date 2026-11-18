"""The stored form of the diary survives a restart unchanged and refuses data it cannot trust."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from custom_components.baby_feeding.diary import Feed, FeedingState
from custom_components.baby_feeding.persistence import from_stored, to_stored
from custom_components.baby_feeding.planning import Plan
from custom_components.baby_feeding.schedule import NightRhythm

AMSTERDAM = ZoneInfo('Europe/Amsterdam')


def local(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=AMSTERDAM)


FULL = FeedingState(
    feeds=(Feed(feed_id='a', start=local('2026-11-14T10:00:47'), amount=60), Feed(feed_id='b', start=local('2026-11-14T13:00'), amount=70)),
    plan=Plan(feed_id='b', feed_start=local('2026-11-14T13:00'), due=local('2026-11-14T16:00'), alerted=True, claimed=True),
    pending=local('2026-11-14T16:00'),
    night_rhythm=NightRhythm(custom_enabled=True, custom_hours=6),
    standard_amount=70,
    maximum_amount=90,
)


@pytest.mark.parametrize('state', [FeedingState(), FULL])
def test_a_stored_state_reads_back_identically(state: FeedingState) -> None:
    assert from_stored(to_stored(state)) == state


def test_stored_moments_keep_their_exact_instant() -> None:
    stored = to_stored(FULL)
    assert from_stored(stored).feeds[0].start.timestamp() == local('2026-11-14T10:00:47').timestamp()


@pytest.mark.parametrize('broken', [{'feeds': [{'feed_id': 'a', 'start': '2026-11-14T10:00:00', 'amount': 60}]}, {'feeds': [{'feed_id': 'a', 'start': '2026-11-14T10:00:00+01:00', 'amount': -5}]}])
def test_untrustworthy_stored_data_is_refused(broken: dict) -> None:
    with pytest.raises(ValueError):
        from_stored(broken)
