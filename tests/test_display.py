"""What the widgets and the lock screen show for the current plan."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from custom_components.baby_feeding.display import lock_screen_message, next_bottle_text, progress_percent
from custom_components.baby_feeding.planning import Plan

AMSTERDAM = ZoneInfo('Europe/Amsterdam')
DASHBOARD = '/dashboard-main/voeding'
STYLE = {
    'notification_icon': 'mdi:baby-bottle-outline', 'notification_icon_color': '#D88959', 'background_color': '#1C1C1E',
    'text_color': '#E8E2DC', 'progress_bar_color': '#D88959', 'url': DASHBOARD,
}


def local(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=AMSTERDAM)


def plan(*, start: str, due: str, alerted: bool = False) -> Plan:
    return Plan(feed_id='feed-1', feed_start=local(start), due=local(due), alerted=alerted, claimed=alerted)


@pytest.mark.parametrize(('due', 'expected'), [('2026-11-14T14:12', '14:12'), ('2026-11-15T03:10', '03:10'), ('2026-11-14T12:38', 'Now'), ('2026-11-14T11:00', 'Now')])
def test_next_bottle_text_shows_the_local_clock_time_or_now(due: str, expected: str) -> None:
    current = plan(start='2026-11-14T09:00', due=due)
    assert next_bottle_text(plan=current, now=local('2026-11-14T12:38'), time_zone=AMSTERDAM, language='en') == expected


def test_next_bottle_text_without_a_plan() -> None:
    assert next_bottle_text(plan=None, now=local('2026-11-14T12:38'), time_zone=AMSTERDAM, language='en') == 'Not planned'


@pytest.mark.parametrize(
    ('now', 'expected'),
    [
        ('2026-11-14T10:00:00', 0), ('2026-11-14T10:08:59', 0), ('2026-11-14T10:09:00', 5), ('2026-11-14T11:30:00', 50),
        ('2026-11-14T12:59:59', 95), ('2026-11-14T13:00:00', 100), ('2026-11-14T15:00:00', 100), ('2026-11-14T09:00:00', 0),
    ],
)
def test_progress_fills_in_steps_of_five(now: str, expected: int) -> None:
    assert progress_percent(plan=plan(start='2026-11-14T10:00', due='2026-11-14T13:00'), now=local(now)) == expected


def test_progress_without_a_plan_is_empty() -> None:
    assert progress_percent(plan=None, now=local('2026-11-14T11:30')) == 0


def test_lock_screen_counts_down_to_the_next_bottle() -> None:
    message = lock_screen_message(plan=plan(start='2026-11-14T17:00', due='2026-11-14T20:00'), now=local('2026-11-14T17:30'), time_zone=AMSTERDAM, dashboard_url=DASHBOARD, language='en')
    assert message == {
        'title': 'Next bottle',
        'message': 'at 20:00 · last bottle 17:00',
        'data': {
            'tag': 'baby_feeding', 'live_update': True, 'silent': True, 'chronometer': True, 'when': 9000, 'when_relative': True,
            'critical_text': '20:00', 'progress_bar_direction': 'increasing', **STYLE,
        },
    }


def test_lock_screen_names_a_bottle_that_is_set_ahead() -> None:
    message = lock_screen_message(plan=plan(start='2026-11-14T17:10', due='2026-11-14T20:10'), now=local('2026-11-14T16:50'), time_zone=AMSTERDAM, dashboard_url=DASHBOARD, language='en')
    assert message['message'] == 'at 20:10 · bottle at 17:10'
    assert message['data']['when'] == 12000


@pytest.mark.parametrize('due', ['2026-11-14T17:30', '2026-11-14T17:20'])
def test_lock_screen_shows_that_the_bottle_is_due(due: str) -> None:
    message = lock_screen_message(plan=plan(start='2026-11-14T14:30', due=due), now=local('2026-11-14T17:30'), time_zone=AMSTERDAM, dashboard_url=DASHBOARD, language='en')
    assert message == {
        'title': 'Next bottle',
        'message': 'Time for the bottle',
        'data': {'tag': 'baby_feeding', 'live_update': True, 'silent': True, 'progress': 1, 'progress_max': 1, 'critical_text': 'Now', **STYLE},
    }


def test_lock_screen_stays_untouched_without_a_plan() -> None:
    assert lock_screen_message(plan=None, now=local('2026-11-14T17:30'), time_zone=AMSTERDAM, dashboard_url=DASHBOARD, language='en') is None


@pytest.mark.parametrize(('language', 'texts'), [
    ('nl', ('Niet gepland', 'om 20:00 · laatste fles 17:00', 'Volgende fles')),
    ('nl-BE', ('Niet gepland', 'om 20:00 · laatste fles 17:00', 'Volgende fles')),
    ('de', ('Not planned', 'at 20:00 · last bottle 17:00', 'Next bottle')),
])
def test_texts_follow_the_home_assistant_language_with_english_as_fallback(language: str, texts: tuple[str, str, str]) -> None:
    not_planned, countdown, title = texts
    assert next_bottle_text(plan=None, now=local('2026-11-14T17:30'), time_zone=AMSTERDAM, language=language) == not_planned
    message = lock_screen_message(plan=plan(start='2026-11-14T17:00', due='2026-11-14T20:00'), now=local('2026-11-14T17:30'), time_zone=AMSTERDAM, dashboard_url=DASHBOARD, language=language)
    assert (message['message'], message['title']) == (countdown, title)
