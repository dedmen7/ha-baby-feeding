"""The feeding diary: saved bottles, the plan for the next one and the rules for changing them."""

from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .planning import Plan, alert_is_due, mark_alerted, move_feed, plan_for_feed, replan
from .schedule import NightRhythm

MAXIMUM_AMOUNT = 9999
DEFAULT_STANDARD_AMOUNT = 20
AHEAD_LIMIT = timedelta(hours=24)


class FeedError(ValueError):
    """A diary change that is refused, with a message the parents can act on."""


@dataclass(frozen=True)
class Feed:
    feed_id: str
    start: datetime
    amount: int


@dataclass(frozen=True)
class FeedingState:
    """Everything the integration stores; `pending` is the start a still open bottle form is prefilled with."""

    feeds: tuple[Feed, ...] = ()
    plan: Plan | None = None
    pending: datetime | None = None
    night_rhythm: NightRhythm = NightRhythm()
    standard_amount: int = DEFAULT_STANDARD_AMOUNT
    maximum_amount: int | None = None


def save_bottle(state: FeedingState, *, start: datetime, amount: int, now: datetime, time_zone: ZoneInfo, new_id: Callable[[], str]) -> FeedingState:
    if start > now + AHEAD_LIMIT:
        raise FeedError('Vul een begintijd tot uiterlijk 24 uur vooruit in.')
    feed = Feed(feed_id=new_id(), start=start, amount=valid_amount(amount))
    _ensure_free_minute(feeds=state.feeds, start=start, ignore_id=None)
    plan = _plan_from(plan=state.plan, feed=feed, night_rhythm=state.night_rhythm, time_zone=time_zone)
    return replace(state, feeds=_sorted((*state.feeds, feed)), plan=plan, pending=None)


def add_earlier_feed(state: FeedingState, *, start: datetime, amount: int, now: datetime, new_id: Callable[[], str]) -> FeedingState:
    if start > now:
        raise FeedError('Vul een verstreken begintijd in. Zet een fles vooruit via Fles invullen.')
    feed = Feed(feed_id=new_id(), start=start, amount=valid_amount(amount))
    _ensure_free_minute(feeds=state.feeds, start=start, ignore_id=None)
    return replace(state, feeds=_sorted((*state.feeds, feed)))


def update_feed(state: FeedingState, *, feed_id: str, start: datetime, amount: int, now: datetime, time_zone: ZoneInfo) -> FeedingState:
    original = _find(feeds=state.feeds, feed_id=feed_id)
    is_planned = state.plan is not None and state.plan.feed_id == feed_id
    moved = start != original.start
    if moved and start > now + AHEAD_LIMIT:
        raise FeedError('Kies een tijdstip tot uiterlijk 24 uur vooruit.')
    if moved and start > now and not is_planned:
        raise FeedError('Kies een tijdstip dat al voorbij is. Alleen de laatst opgeslagen fles kan vooruit staan.')
    _ensure_free_minute(feeds=state.feeds, start=start, ignore_id=feed_id)
    changed = Feed(feed_id=feed_id, start=start, amount=valid_amount(amount))
    feeds = _sorted(tuple(changed if feed.feed_id == feed_id else feed for feed in state.feeds))
    if not (is_planned and moved):
        return replace(state, feeds=feeds)
    newest = _newest(feeds=feeds, now=now)
    plan = _plan_from(plan=state.plan, feed=newest, night_rhythm=state.night_rhythm, time_zone=time_zone)
    return replace(state, feeds=feeds, plan=plan)


def delete_feed(state: FeedingState, *, feed_id: str, now: datetime, time_zone: ZoneInfo) -> FeedingState:
    _find(feeds=state.feeds, feed_id=feed_id)
    feeds = tuple(feed for feed in state.feeds if feed.feed_id != feed_id)
    if state.plan is None or state.plan.feed_id != feed_id:
        return replace(state, feeds=feeds)
    newest = _newest(feeds=feeds, now=now)
    plan = None if newest is None else _plan_from(plan=None, feed=newest, night_rhythm=state.night_rhythm, time_zone=time_zone)
    return replace(state, feeds=feeds, plan=plan)


def alert(state: FeedingState, *, now: datetime) -> tuple[FeedingState, bool]:
    if state.plan is None or not alert_is_due(plan=state.plan, now=now):
        return state, False
    return replace(state, plan=mark_alerted(state.plan), pending=state.pending or state.plan.due), True


def open_new_bottle(state: FeedingState, *, now: datetime) -> FeedingState:
    if state.pending is not None:
        return state
    return replace(state, pending=now.replace(second=0, microsecond=0))


def set_night_rhythm(state: FeedingState, *, night_rhythm: NightRhythm, now: datetime, time_zone: ZoneInfo) -> FeedingState:
    plan = None if state.plan is None else replan(plan=state.plan, night_rhythm=night_rhythm, time_zone=time_zone, now=now)
    return replace(state, night_rhythm=night_rhythm, plan=plan)


def set_amounts(state: FeedingState, *, standard_amount: int, maximum_amount: int | None) -> FeedingState:
    standard = valid_amount(standard_amount)
    maximum = None if maximum_amount is None else valid_amount(maximum_amount)
    if maximum is not None and maximum < 1:
        raise FeedError('Vul een maximum van minstens 1 cc in of laat het leeg.')
    if maximum is not None and standard > maximum:
        raise FeedError('De standaardhoeveelheid ligt boven het afgesproken maximum.')
    return replace(state, standard_amount=standard, maximum_amount=maximum)


def valid_amount(amount: object) -> int:
    if not isinstance(amount, int) or isinstance(amount, bool) or not 0 <= amount <= MAXIMUM_AMOUNT:
        raise FeedError('Vul een heel aantal cc in tussen 0 en 9999.')
    return amount


def _plan_from(*, plan: Plan | None, feed: Feed, night_rhythm: NightRhythm, time_zone: ZoneInfo) -> Plan:
    if plan is None:
        return plan_for_feed(feed_id=feed.feed_id, feed_start=feed.start, night_rhythm=night_rhythm, time_zone=time_zone)
    return move_feed(plan=plan, feed_id=feed.feed_id, feed_start=feed.start, night_rhythm=night_rhythm, time_zone=time_zone)


def _ensure_free_minute(*, feeds: tuple[Feed, ...], start: datetime, ignore_id: str | None) -> None:
    minute = start.replace(second=0, microsecond=0)
    if any(feed.feed_id != ignore_id and feed.start.replace(second=0, microsecond=0) == minute for feed in feeds):
        raise FeedError('Er staat al een voeding op deze minuut. Pas die voeding aan of kies de werkelijke begintijd.')


def _find(*, feeds: tuple[Feed, ...], feed_id: str) -> Feed:
    for feed in feeds:
        if feed.feed_id == feed_id:
            return feed
    raise FeedError('Deze voeding is verplaatst of verwijderd. Vernieuw het overzicht.')


def _newest(*, feeds: tuple[Feed, ...], now: datetime) -> Feed | None:
    candidates = [feed for feed in feeds if feed.start <= now + AHEAD_LIMIT]
    return max(candidates, key=lambda feed: feed.start, default=None)


def _sorted(feeds: tuple[Feed, ...]) -> tuple[Feed, ...]:
    return tuple(sorted(feeds, key=lambda feed: feed.start))
