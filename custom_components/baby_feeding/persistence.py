"""Convert the diary state to and from the JSON stored in Home Assistant's .storage folder."""

from datetime import datetime, time
from typing import Any

from .diary import DEFAULT_STANDARD_AMOUNT, Feed, FeedingState, valid_amount
from .planning import Plan
from .schedule import NightRhythm


def to_stored(state: FeedingState) -> dict[str, Any]:
    return {
        'feeds': [{'feed_id': feed.feed_id, 'start': feed.start.isoformat(), 'amount': feed.amount} for feed in state.feeds],
        'plan': None if state.plan is None else {
            'feed_id': state.plan.feed_id, 'feed_start': state.plan.feed_start.isoformat(), 'due': state.plan.due.isoformat(),
            'alerted': state.plan.alerted, 'claimed': state.plan.claimed,
        },
        'pending': None if state.pending is None else state.pending.isoformat(),
        'night_custom_enabled': state.night_rhythm.custom_enabled,
        'night_hours': state.night_rhythm.custom_hours,
        'night_starts_at': state.night_rhythm.starts_at.strftime('%H:%M'),
        'standard_amount': state.standard_amount,
        'maximum_amount': state.maximum_amount,
    }


def from_stored(data: dict[str, Any]) -> FeedingState:
    feeds = tuple(Feed(feed_id=str(item['feed_id']), start=_moment(item['start']), amount=valid_amount(item['amount'])) for item in data.get('feeds', []))
    stored_plan = data.get('plan')
    plan = None if stored_plan is None else Plan(
        feed_id=str(stored_plan['feed_id']), feed_start=_moment(stored_plan['feed_start']), due=_moment(stored_plan['due']),
        alerted=bool(stored_plan['alerted']), claimed=bool(stored_plan['claimed']),
    )
    pending = data.get('pending')
    maximum = data.get('maximum_amount')
    return FeedingState(
        feeds=feeds,
        plan=plan,
        pending=None if pending is None else _moment(pending),
        night_rhythm=NightRhythm(
            custom_enabled=bool(data.get('night_custom_enabled', False)), custom_hours=data.get('night_hours', 4),
            starts_at=time.fromisoformat(data.get('night_starts_at', '22:30')),
        ),
        standard_amount=valid_amount(data.get('standard_amount', DEFAULT_STANDARD_AMOUNT)),
        maximum_amount=None if maximum is None else valid_amount(maximum),
    )


def _moment(value: str) -> datetime:
    moment = datetime.fromisoformat(value)
    if moment.tzinfo is None:
        raise ValueError('A stored moment has no time zone.')
    return moment
