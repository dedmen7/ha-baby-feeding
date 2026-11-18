"""The plan for the next bottle and the rules that decide when the reminder may sound."""

from dataclasses import dataclass, replace
from datetime import datetime
from zoneinfo import ZoneInfo

from .schedule import NightRhythm, next_due


@dataclass(frozen=True)
class Plan:
    """The bottle the next reminder counts from, with what has already been alerted for it."""

    feed_id: str
    feed_start: datetime
    due: datetime
    alerted: bool = False
    claimed: bool = False


def plan_for_feed(*, feed_id: str, feed_start: datetime, night_rhythm: NightRhythm, time_zone: ZoneInfo) -> Plan:
    due = next_due(start=feed_start, night_rhythm=night_rhythm, time_zone=time_zone)
    return Plan(feed_id=feed_id, feed_start=feed_start, due=due)


def replan(*, plan: Plan, night_rhythm: NightRhythm, time_zone: ZoneInfo, now: datetime) -> Plan:
    due = next_due(start=plan.feed_start, night_rhythm=night_rhythm, time_zone=time_zone)
    if due == plan.due:
        return plan
    # A bottle that already alerted stays quiet for a moment that has passed; a later moment arms a new alert.
    return replace(plan, due=due, alerted=plan.claimed and due <= now)


def move_feed(*, plan: Plan, feed_id: str, feed_start: datetime, night_rhythm: NightRhythm, time_zone: ZoneInfo) -> Plan:
    due = next_due(start=feed_start, night_rhythm=night_rhythm, time_zone=time_zone)
    return Plan(feed_id=feed_id, feed_start=feed_start, due=due, alerted=plan.alerted and due == plan.due)


def alert_is_due(*, plan: Plan, now: datetime) -> bool:
    return not plan.alerted and plan.due <= now


def mark_alerted(plan: Plan) -> Plan:
    return replace(plan, alerted=True, claimed=True)
