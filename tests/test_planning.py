"""Reminder rules: one alert per planned moment and no second alert for a moment that already passed."""

from datetime import datetime
from zoneinfo import ZoneInfo

from custom_components.baby_feeding.planning import Plan, alert_is_due, mark_alerted, move_feed, plan_for_feed, replan
from custom_components.baby_feeding.schedule import NightRhythm

AMSTERDAM = ZoneInfo('Europe/Amsterdam')
DEFAULT_NIGHTS = NightRhythm()
FIVE_HOUR_NIGHTS = NightRhythm(custom_enabled=True, custom_hours=5)


def local(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=AMSTERDAM)


def planned(*, start: str, night_rhythm: NightRhythm = DEFAULT_NIGHTS) -> Plan:
    return plan_for_feed(feed_id='feed-1', feed_start=local(start), night_rhythm=night_rhythm, time_zone=AMSTERDAM)


def alert_when_due(*, plan: Plan, now: datetime) -> tuple[Plan, int]:
    if alert_is_due(plan=plan, now=now):
        return mark_alerted(plan), 1
    return plan, 0


def with_nights(*, plan: Plan, night_rhythm: NightRhythm, now: datetime) -> Plan:
    return replan(plan=plan, night_rhythm=night_rhythm, time_zone=AMSTERDAM, now=now)


def test_a_new_bottle_is_planned_from_its_own_start() -> None:
    plan = planned(start='2026-11-14T22:30')
    assert plan.feed_id == 'feed-1'
    assert plan.feed_start == local('2026-11-14T22:30')
    assert plan.due == local('2026-11-15T02:30')
    assert (plan.alerted, plan.claimed) == (False, False)


def test_the_alert_fires_once_when_the_planned_moment_arrives() -> None:
    plan = planned(start='2026-11-14T22:30')
    assert not alert_is_due(plan=plan, now=local('2026-11-15T02:29:59'))
    plan, alerts = alert_when_due(plan=plan, now=local('2026-11-15T02:30'))
    assert alerts == 1
    assert (plan.alerted, plan.claimed) == (True, True)
    assert not alert_is_due(plan=plan, now=local('2026-11-15T02:31'))


def test_saving_unchanged_night_settings_keeps_the_alert_state() -> None:
    now = local('2026-11-15T03:35')
    plan, _ = alert_when_due(plan=planned(start='2026-11-14T22:30', night_rhythm=FIVE_HOUR_NIGHTS), now=now)
    assert with_nights(plan=plan, night_rhythm=FIVE_HOUR_NIGHTS, now=now) == plan


def test_changing_to_another_passed_moment_does_not_alert_again() -> None:
    now = local('2026-11-15T03:35')
    plan, alerts = alert_when_due(plan=planned(start='2026-11-14T22:30', night_rhythm=FIVE_HOUR_NIGHTS), now=now)
    for night_rhythm, due in [(DEFAULT_NIGHTS, '02:30'), (FIVE_HOUR_NIGHTS, '03:30'), (DEFAULT_NIGHTS, '02:30'), (FIVE_HOUR_NIGHTS, '03:30')]:
        plan = with_nights(plan=plan, night_rhythm=night_rhythm, now=now)
        assert plan.due == local('2026-11-15T' + due)
        assert plan.alerted
        plan, extra = alert_when_due(plan=plan, now=now)
        alerts += extra
    assert alerts == 1


def test_postponing_an_alerted_bottle_arms_exactly_one_new_alert() -> None:
    plan, alerts = alert_when_due(plan=planned(start='2026-11-14T22:30'), now=local('2026-11-15T02:35'))
    plan = with_nights(plan=plan, night_rhythm=FIVE_HOUR_NIGHTS, now=local('2026-11-15T02:35'))
    assert plan.due == local('2026-11-15T03:30')
    assert (plan.alerted, plan.claimed) == (False, True)
    plan, extra = alert_when_due(plan=plan, now=local('2026-11-15T02:35'))
    alerts += extra
    for _ in range(2):
        plan, extra = alert_when_due(plan=plan, now=local('2026-11-15T03:30'))
        alerts += extra
        plan = with_nights(plan=plan, night_rhythm=FIVE_HOUR_NIGHTS, now=local('2026-11-15T03:30'))
    assert alerts == 2
    assert plan.alerted


def test_returning_to_the_alerted_passed_moment_stays_quiet_until_the_new_moment() -> None:
    now = local('2026-11-15T02:35')
    plan, alerts = alert_when_due(plan=planned(start='2026-11-14T22:30'), now=now)
    plan = with_nights(plan=plan, night_rhythm=FIVE_HOUR_NIGHTS, now=now)
    for night_rhythm, alerted in [(DEFAULT_NIGHTS, True), (FIVE_HOUR_NIGHTS, False), (DEFAULT_NIGHTS, True), (FIVE_HOUR_NIGHTS, False)]:
        plan = with_nights(plan=plan, night_rhythm=night_rhythm, now=now)
        assert plan.alerted is alerted
        plan, extra = alert_when_due(plan=plan, now=now)
        alerts += extra
    assert alerts == 1
    for _ in range(2):
        plan, extra = alert_when_due(plan=plan, now=local('2026-11-15T03:30'))
        alerts += extra
    assert alerts == 2


def test_a_bottle_that_never_alerted_alerts_when_new_settings_make_it_due() -> None:
    now = local('2026-11-15T02:35')
    plan = with_nights(plan=planned(start='2026-11-14T22:30', night_rhythm=FIVE_HOUR_NIGHTS), night_rhythm=DEFAULT_NIGHTS, now=now)
    assert plan.due == local('2026-11-15T02:30')
    alerts = 0
    for _ in range(2):
        plan, extra = alert_when_due(plan=plan, now=now)
        alerts += extra
    assert alerts == 1


def test_moving_the_bottle_resets_its_alert_history() -> None:
    plan, _ = alert_when_due(plan=planned(start='2026-11-14T22:30'), now=local('2026-11-15T02:35'))
    plan = with_nights(plan=plan, night_rhythm=FIVE_HOUR_NIGHTS, now=local('2026-11-15T02:35'))
    assert plan.claimed
    plan = move_feed(plan=plan, feed_id='feed-1', feed_start=local('2026-11-14T23:00'), night_rhythm=FIVE_HOUR_NIGHTS, time_zone=AMSTERDAM)
    assert plan.due == local('2026-11-15T04:00')
    assert (plan.alerted, plan.claimed) == (False, False)
    plan = with_nights(plan=plan, night_rhythm=DEFAULT_NIGHTS, now=local('2026-11-15T03:10'))
    assert plan.due == local('2026-11-15T03:00')
    assert alert_is_due(plan=plan, now=local('2026-11-15T03:10'))


def test_moving_the_bottle_stays_quiet_when_the_planned_moment_does_not_change() -> None:
    plan, _ = alert_when_due(plan=planned(start='2026-11-14T06:30'), now=local('2026-11-14T10:30'))
    moved = move_feed(plan=plan, feed_id='feed-1', feed_start=local('2026-11-14T07:30'), night_rhythm=DEFAULT_NIGHTS, time_zone=AMSTERDAM)
    assert moved.feed_start == local('2026-11-14T07:30')
    assert moved.due == plan.due
    assert moved.alerted
    assert not alert_is_due(plan=moved, now=local('2026-11-14T10:31'))


def test_handing_the_plan_to_another_bottle_starts_from_that_bottle() -> None:
    plan = planned(start='2026-11-14T13:00')
    handed = move_feed(plan=plan, feed_id='feed-2', feed_start=local('2026-11-14T10:00'), night_rhythm=DEFAULT_NIGHTS, time_zone=AMSTERDAM)
    assert (handed.feed_id, handed.due) == ('feed-2', local('2026-11-14T13:00'))
    assert (handed.alerted, handed.claimed) == (False, False)
