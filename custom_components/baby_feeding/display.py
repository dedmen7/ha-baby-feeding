"""What widgets and the lock screen show for the plan: plain texts and the Live Activity message."""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .planning import Plan

LIVE_ACTIVITY_TAG = 'voeding'
TITLE = 'Volgende fles'
NOT_PLANNED = 'Niet gepland'
NOW = 'Nu'
STYLE = {
    'notification_icon': 'mdi:baby-bottle-outline',
    'notification_icon_color': '#D88959',
    'background_color': '#1C1C1E',
    'text_color': '#E8E2DC',
    'progress_bar_color': '#D88959',
}


def next_bottle_text(*, plan: Plan | None, now: datetime, time_zone: ZoneInfo) -> str:
    if plan is None:
        return NOT_PLANNED
    return _clock(moment=plan.due, time_zone=time_zone) if plan.due > now else NOW


def progress_percent(*, plan: Plan | None, now: datetime) -> int:
    if plan is None or plan.due <= plan.feed_start:
        return 0
    elapsed = (now - plan.feed_start).total_seconds()
    span = (plan.due - plan.feed_start).total_seconds()
    # Steps of five keep widget refreshes rare without hiding real progress.
    return max(0, min(100, int(elapsed * 20 // span) * 5))


def lock_screen_message(*, plan: Plan | None, now: datetime, time_zone: ZoneInfo, dashboard_url: str) -> dict[str, Any] | None:
    if plan is None:
        return None
    base = {'tag': LIVE_ACTIVITY_TAG, 'live_update': True, 'silent': True}
    style = {**STYLE, 'url': dashboard_url}
    if plan.due <= now:
        data = {**base, 'progress': 1, 'progress_max': 1, 'critical_text': NOW, **style}
        return {'title': TITLE, 'message': 'Tijd voor de fles', 'data': data}
    due_clock = _clock(moment=plan.due, time_zone=time_zone)
    feed_label = 'fles om ' if plan.feed_start > now else 'laatste fles '
    data = {
        **base, 'chronometer': True, 'when': int((plan.due - now).total_seconds()), 'when_relative': True,
        'critical_text': due_clock, 'progress_bar_direction': 'increasing', **style,
    }
    message = 'om ' + due_clock + ' · ' + feed_label + _clock(moment=plan.feed_start, time_zone=time_zone)
    return {'title': TITLE, 'message': message, 'data': data}


def _clock(*, moment: datetime, time_zone: ZoneInfo) -> str:
    return moment.astimezone(time_zone).strftime('%H:%M')
