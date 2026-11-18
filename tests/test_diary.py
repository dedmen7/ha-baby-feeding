"""Diary rules: which bottles may be saved, which bottle drives the reminder, and when the form opens again."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from custom_components.baby_feeding.diary import (
    Feed,
    FeedError,
    FeedingState,
    add_earlier_feed,
    alert,
    delete_feed,
    open_new_bottle,
    save_bottle,
    set_night_rhythm,
    update_feed,
)
from custom_components.baby_feeding.schedule import NightRhythm

AMSTERDAM = ZoneInfo('Europe/Amsterdam')


def local(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=AMSTERDAM)


def ids() -> object:
    counter = iter(range(1, 1000))
    return lambda: 'feed-' + str(next(counter))


def bottle(state: FeedingState, *, start: str, amount: int = 70, now: str, new_id: object) -> FeedingState:
    return save_bottle(state, start=local(start), amount=amount, now=local(now), time_zone=AMSTERDAM, new_id=new_id)


def test_saving_a_bottle_stores_it_and_plans_the_next_one() -> None:
    new_id = ids()
    state = bottle(FeedingState(), start='2026-11-14T11:12', amount=30, now='2026-11-14T12:38', new_id=new_id)
    assert state.feeds == (Feed(feed_id='feed-1', start=local('2026-11-14T11:12'), amount=30),)
    assert (state.plan.feed_id, state.plan.due) == ('feed-1', local('2026-11-14T14:12'))
    assert state.pending is None


@pytest.mark.parametrize(('start', 'due'), [('2026-11-14T17:10', '2026-11-14T20:10'), ('2026-11-14T22:45', '2026-11-15T02:45'), ('2026-11-15T16:50', '2026-11-15T19:50')])
def test_a_bottle_may_be_set_up_to_24_hours_ahead(start: str, due: str) -> None:
    state = bottle(FeedingState(), start=start, now='2026-11-14T16:50', new_id=ids())
    assert state.plan.due == local(due)


def test_a_bottle_more_than_24_hours_ahead_is_refused() -> None:
    with pytest.raises(FeedError, match='24 uur'):
        bottle(FeedingState(), start='2026-11-15T16:51', now='2026-11-14T16:50', new_id=ids())


@pytest.mark.parametrize('amount', [-1, 10000, 2.5, '20', None, True])
def test_only_whole_amounts_from_0_to_9999_are_accepted(amount: object) -> None:
    with pytest.raises(FeedError, match='0 en 9999'):
        bottle(FeedingState(), start='2026-11-14T11:12', amount=amount, now='2026-11-14T12:38', new_id=ids())


@pytest.mark.parametrize('amount', [0, 20, 9999])
def test_boundary_amounts_are_accepted(amount: int) -> None:
    assert bottle(FeedingState(), start='2026-11-14T11:12', amount=amount, now='2026-11-14T12:38', new_id=ids()).feeds[0].amount == amount


def test_a_second_bottle_in_the_same_minute_is_refused() -> None:
    new_id = ids()
    state = bottle(FeedingState(), start='2026-11-14T11:12', now='2026-11-14T12:38', new_id=new_id)
    with pytest.raises(FeedError, match='minuut'):
        add_earlier_feed(state, start=local('2026-11-14T11:12:30'), amount=30, now=local('2026-11-14T12:38'), new_id=new_id)


def test_an_earlier_feed_must_have_passed_and_leaves_the_reminder_alone() -> None:
    new_id = ids()
    state = bottle(FeedingState(), start='2026-11-14T11:12', now='2026-11-14T15:00', new_id=new_id)
    with pytest.raises(FeedError, match='verstreken'):
        add_earlier_feed(state, start=local('2026-11-14T15:10'), amount=30, now=local('2026-11-14T15:00'), new_id=new_id)
    later = add_earlier_feed(state, start=local('2026-11-14T12:00'), amount=20, now=local('2026-11-14T15:00'), new_id=new_id)
    assert len(later.feeds) == 2
    assert later.plan == state.plan


def test_changing_only_the_amount_keeps_the_plan() -> None:
    state = bottle(FeedingState(), start='2026-11-14T11:12', now='2026-11-14T12:38', new_id=ids())
    changed = update_feed(state, feed_id='feed-1', start=local('2026-11-14T11:12'), amount=45, now=local('2026-11-14T12:38'), time_zone=AMSTERDAM)
    assert changed.feeds[0].amount == 45
    assert changed.plan == state.plan


def test_moving_the_planned_bottle_earlier_hands_the_plan_to_a_newer_feed() -> None:
    new_id = ids()
    state = bottle(FeedingState(), start='2026-11-14T13:00', now='2026-11-14T15:00', new_id=new_id)
    state = add_earlier_feed(state, start=local('2026-11-14T10:00'), amount=30, now=local('2026-11-14T15:00'), new_id=new_id)
    moved = update_feed(state, feed_id='feed-1', start=local('2026-11-14T08:00'), amount=70, now=local('2026-11-14T15:00'), time_zone=AMSTERDAM)
    assert (moved.plan.feed_id, moved.plan.due) == ('feed-2', local('2026-11-14T13:00'))


@pytest.mark.parametrize(('moved', 'due'), [('2026-11-14T17:30', '2026-11-14T20:30'), ('2026-11-15T16:50', '2026-11-15T19:50'), ('2026-11-14T16:45', '2026-11-14T19:45')])
def test_the_planned_bottle_may_move_ahead_and_still_drives_the_reminder(moved: str, due: str) -> None:
    new_id = ids()
    state = add_earlier_feed(FeedingState(), start=local('2026-11-14T14:00'), amount=70, now=local('2026-11-14T16:50'), new_id=new_id)
    state = bottle(state, start='2026-11-14T17:10', now='2026-11-14T16:50', new_id=new_id)
    moved_state = update_feed(state, feed_id='feed-2', start=local(moved), amount=70, now=local('2026-11-14T16:50'), time_zone=AMSTERDAM)
    assert (moved_state.plan.feed_id, moved_state.plan.due) == ('feed-2', local(due))


def test_an_older_feed_cannot_move_ahead() -> None:
    new_id = ids()
    state = add_earlier_feed(FeedingState(), start=local('2026-11-14T11:00'), amount=60, now=local('2026-11-14T16:50'), new_id=new_id)
    state = bottle(state, start='2026-11-14T14:00', now='2026-11-14T16:50', new_id=new_id)
    with pytest.raises(FeedError, match='laatst opgeslagen fles'):
        update_feed(state, feed_id='feed-1', start=local('2026-11-14T17:45'), amount=60, now=local('2026-11-14T16:50'), time_zone=AMSTERDAM)


def test_an_unknown_feed_cannot_be_changed() -> None:
    with pytest.raises(FeedError, match='verwijderd'):
        update_feed(FeedingState(), feed_id='feed-9', start=local('2026-11-14T11:00'), amount=60, now=local('2026-11-14T16:50'), time_zone=AMSTERDAM)


def test_deleting_the_planned_bottle_plans_from_the_newest_remaining_feed() -> None:
    new_id = ids()
    state = add_earlier_feed(FeedingState(), start=local('2026-11-14T10:00'), amount=60, now=local('2026-11-14T16:50'), new_id=new_id)
    state = bottle(state, start='2026-11-14T14:00', now='2026-11-14T16:50', new_id=new_id)
    remaining = delete_feed(state, feed_id='feed-2', now=local('2026-11-14T16:50'), time_zone=AMSTERDAM)
    assert (remaining.plan.feed_id, remaining.plan.due) == ('feed-1', local('2026-11-14T13:00'))
    assert delete_feed(remaining, feed_id='feed-1', now=local('2026-11-14T16:50'), time_zone=AMSTERDAM).plan is None


def test_the_reminder_alerts_once_and_opens_the_form_at_the_planned_time() -> None:
    state = bottle(FeedingState(), start='2026-11-14T11:12', now='2026-11-14T12:38', new_id=ids())
    state, alerted = alert(state, now=local('2026-11-14T14:11'))
    assert not alerted
    state, alerted = alert(state, now=local('2026-11-14T14:12'))
    assert alerted
    assert state.pending == local('2026-11-14T14:12')
    state, alerted = alert(state, now=local('2026-11-14T14:20'))
    assert not alerted


def test_a_new_bottle_opens_the_form_at_the_current_minute_once() -> None:
    state = bottle(FeedingState(), start='2026-11-14T11:12', now='2026-11-14T12:38', new_id=ids())
    opened = open_new_bottle(state, now=local('2026-11-14T12:38:41'))
    assert opened.pending == local('2026-11-14T12:38')
    assert open_new_bottle(opened, now=local('2026-11-14T13:00')).pending == local('2026-11-14T12:38')


def test_night_settings_replan_from_the_saved_bottle_without_touching_the_diary() -> None:
    state = bottle(FeedingState(), start='2026-11-14T23:17', amount=45, now='2026-11-15T01:11', new_id=ids())
    for rhythm, due in [(NightRhythm(custom_enabled=True, custom_hours=5), '04:17'), (NightRhythm(custom_enabled=False, custom_hours=5), '03:17')]:
        changed = set_night_rhythm(state, night_rhythm=rhythm, now=local('2026-11-15T01:11'), time_zone=AMSTERDAM)
        assert changed.plan.due == local('2026-11-15T' + due)
        assert changed.feeds == state.feeds
        assert changed.night_rhythm == rhythm


def test_the_plan_counts_from_a_bottle_saved_via_fles_invullen_even_if_an_earlier_feed_is_newer() -> None:
    new_id = ids()
    state = add_earlier_feed(FeedingState(), start=local('2026-11-14T12:00'), amount=20, now=local('2026-11-14T15:00'), new_id=new_id)
    state = bottle(state, start='2026-11-14T11:12', now='2026-11-14T15:00', new_id=new_id)
    assert state.plan.feed_id == 'feed-2'
    assert state.plan.due == local('2026-11-14T11:12') + timedelta(hours=3)
