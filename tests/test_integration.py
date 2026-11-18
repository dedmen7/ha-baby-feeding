"""The integration in a running Home Assistant: actions, entities, reminders and phone updates."""

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_fire_time_changed

from custom_components.baby_feeding.const import DOMAIN

from .conftest import DASHBOARD, PHONES, local, pushes

REMINDER = {
    'title': 'Time for the bottle',
    'message': 'Fill in the amount drunk and tap Save.',
    'data': {'url': DASHBOARD, 'push': {'sound': {'name': 'default', 'critical': 1, 'volume': 1.0}}},
}


async def call(hass: HomeAssistant, service: str, **data: object) -> dict | None:
    return await hass.services.async_call(DOMAIN, service, data, blocking=True, return_response=True)


async def advance(hass: HomeAssistant, freezer: FrozenDateTimeFactory, *, to: str) -> None:
    freezer.move_to(local(to))
    async_fire_time_changed(hass, local(to))
    await hass.async_block_till_done()


def state(hass: HomeAssistant, entity_id: str) -> str:
    return hass.states.get(entity_id).state


async def test_entities_start_without_a_plan(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    assert state(hass, 'sensor.baby_feeding_next_bottle') == 'Not planned'
    assert state(hass, 'sensor.baby_feeding_progress') == '0'
    assert state(hass, 'sensor.baby_feeding_next_feeding') == 'unknown'
    status = hass.states.get('sensor.baby_feeding_status')
    assert status.state == 'open'
    assert status.attributes['standard_amount'] == 20
    assert hass.states.get('calendar.baby_feeding_diary') is not None


async def test_saving_a_bottle_plans_the_next_one_and_shows_it_everywhere(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    response = await call(hass, 'save_bottle', start='2026-11-14T11:12:00+01:00', amount=30)
    assert response['next_due'] == local('2026-11-14T14:12').isoformat()
    assert state(hass, 'sensor.baby_feeding_next_bottle') == '14:12'
    assert dt_util.parse_datetime(state(hass, 'sensor.baby_feeding_next_feeding')) == local('2026-11-14T14:12')
    assert state(hass, 'sensor.baby_feeding_progress') == '45'
    status = hass.states.get('sensor.baby_feeding_status')
    assert status.state == 'saved'
    assert status.attributes['plan']['due'] == local('2026-11-14T14:12').isoformat()
    events = await hass.services.async_call(
        'calendar', 'get_events', {'entity_id': 'calendar.baby_feeding_diary', 'start_date_time': local('2026-11-14T00:00'), 'end_date_time': local('2026-11-15T00:00')},
        blocking=True, return_response=True,
    )
    assert [(event['summary'], event['start']) for event in events['calendar.baby_feeding_diary']['events']] == [('30 ml', local('2026-11-14T11:12').isoformat())]


async def test_a_refused_bottle_explains_why_and_changes_nothing(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    with pytest.raises(ServiceValidationError, match='24 hours'):
        await call(hass, 'save_bottle', start='2026-11-15T12:39:00+01:00', amount=30)
    assert state(hass, 'sensor.baby_feeding_next_bottle') == 'Not planned'


async def test_the_reminder_alerts_both_phones_once_at_the_planned_moment(hass: HomeAssistant, entry: MockConfigEntry, phones: dict[str, list[ServiceCall]], freezer: FrozenDateTimeFactory) -> None:
    await call(hass, 'save_bottle', start='2026-11-14T11:12:00+01:00', amount=30)
    await advance(hass, freezer, to='2026-11-14T14:11:59')
    assert not [push for push in pushes(phones) if push[1] == REMINDER]
    await advance(hass, freezer, to='2026-11-14T14:12:00')
    await advance(hass, freezer, to='2026-11-14T14:20:00')
    assert sorted(phone for phone, data in pushes(phones) if data == REMINDER) == PHONES
    status = hass.states.get('sensor.baby_feeding_status')
    assert status.state == 'open'
    assert status.attributes['open_start'] == local('2026-11-14T14:12').isoformat()
    assert state(hass, 'sensor.baby_feeding_next_bottle') == 'Now'


async def test_phones_get_a_silent_countdown_and_a_widget_refresh_after_a_change(hass: HomeAssistant, entry: MockConfigEntry, phones: dict[str, list[ServiceCall]], freezer: FrozenDateTimeFactory) -> None:
    await call(hass, 'save_bottle', start='2026-11-14T12:30:00+01:00', amount=70)
    await advance(hass, freezer, to='2026-11-14T12:38:06')
    countdowns = [(phone, data) for phone, data in pushes(phones) if data.get('data', {}).get('tag') == 'baby_feeding']
    assert sorted(phone for phone, _ in countdowns) == PHONES
    for _, data in countdowns:
        assert data['message'] == 'at 15:30 · last bottle 12:30'
        assert data['data']['silent'] is True
        assert data['data']['url'] == DASHBOARD
    assert sorted(phone for phone, data in pushes(phones) if data == {'message': 'update_widgets'}) == PHONES
    await advance(hass, freezer, to='2026-11-14T12:50:00')
    assert len(pushes(phones)) == 4


async def test_a_burst_of_changes_sends_one_countdown_per_phone(hass: HomeAssistant, entry: MockConfigEntry, phones: dict[str, list[ServiceCall]], freezer: FrozenDateTimeFactory) -> None:
    await call(hass, 'save_bottle', start='2026-11-14T12:30:00+01:00', amount=70)
    await call(hass, 'update_feed', feed_id=hass.states.get('sensor.baby_feeding_status').attributes['plan']['feed_id'], start='2026-11-14T12:31:00+01:00', amount=75)
    await advance(hass, freezer, to='2026-11-14T12:38:06')
    countdowns = [data['message'] for _, data in pushes(phones) if data.get('data', {}).get('tag') == 'baby_feeding']
    assert countdowns == ['at 15:31 · last bottle 12:31'] * 2


async def test_the_diary_survives_a_restart(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    await call(hass, 'save_bottle', start='2026-11-14T11:12:00+01:00', amount=30)
    assert await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert state(hass, 'sensor.baby_feeding_next_bottle') == '14:12'


async def test_a_reminder_missed_during_a_restart_still_alerts_once(hass: HomeAssistant, entry: MockConfigEntry, phones: dict[str, list[ServiceCall]], freezer: FrozenDateTimeFactory) -> None:
    await call(hass, 'save_bottle', start='2026-11-14T11:12:00+01:00', amount=30)
    await hass.config_entries.async_unload(entry.entry_id)
    freezer.move_to(local('2026-11-14T14:30'))
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    await advance(hass, freezer, to='2026-11-14T14:31')
    assert sorted(phone for phone, data in pushes(phones) if data == REMINDER) == PHONES


async def test_settings_change_the_rhythm_and_the_amounts(hass: HomeAssistant, entry: MockConfigEntry, freezer: FrozenDateTimeFactory) -> None:
    freezer.move_to(local('2026-11-15T01:11'))
    await call(hass, 'save_bottle', start='2026-11-14T23:17:00+01:00', amount=45)
    await call(hass, 'set_settings', standard_amount=50, maximum_amount=90, night_custom_enabled=True, night_hours=5)
    assert state(hass, 'sensor.baby_feeding_next_bottle') == '04:17'
    attributes = hass.states.get('sensor.baby_feeding_status').attributes
    assert (attributes['standard_amount'], attributes['maximum_amount'], attributes['night_custom_enabled'], attributes['night_hours']) == (50, 90, True, 5)
    with pytest.raises(ServiceValidationError, match='maximum'):
        await call(hass, 'set_settings', standard_amount=100, maximum_amount=90, night_custom_enabled=True, night_hours=5)


async def test_editing_and_deleting_feeds(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    await call(hass, 'add_earlier_feed', start='2026-11-14T08:00:00+01:00', amount=60)
    await call(hass, 'save_bottle', start='2026-11-14T11:00:00+01:00', amount=70)
    feeds = hass.states.get('sensor.baby_feeding_status').attributes['feeds']
    assert [(feed['amount'], feed['start']) for feed in feeds] == [(60, local('2026-11-14T08:00').isoformat()), (70, local('2026-11-14T11:00').isoformat())]
    await call(hass, 'delete_feed', feed_id=feeds[1]['id'])
    assert hass.states.get('sensor.baby_feeding_status').attributes['plan']['feed_id'] == feeds[0]['id']
    assert state(hass, 'sensor.baby_feeding_next_bottle') == 'Now'
    with pytest.raises(ServiceValidationError, match='deleted'):
        await call(hass, 'delete_feed', feed_id=feeds[1]['id'])


async def test_a_new_bottle_opens_the_form(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    await call(hass, 'save_bottle', start='2026-11-14T11:12:00+01:00', amount=30)
    await call(hass, 'new_bottle')
    status = hass.states.get('sensor.baby_feeding_status')
    assert (status.state, status.attributes['open_start']) == ('open', local('2026-11-14T12:38').isoformat())


async def test_importing_the_old_calendar_once(hass: HomeAssistant, entry: MockConfigEntry, phones: dict[str, list[ServiceCall]]) -> None:
    old_events = [
        {'summary': '60 cc', 'start': '2026-11-14T08:00:30+01:00', 'end': '2026-11-14T08:01:30+01:00'},
        {'summary': '70 cc', 'start': '2026-11-14T11:00:00+01:00', 'end': '2026-11-14T11:01:00+01:00'},
        {'summary': 'Consultatiebureau', 'start': '2026-11-14T09:00:00+01:00', 'end': '2026-11-14T09:30:00+01:00'},
    ]

    async def get_events(service_call: ServiceCall) -> dict:
        return {'calendar.oud_dagboek': {'events': old_events}}

    hass.services.async_register('calendar', 'get_events', get_events, supports_response='only')
    response = await call(hass, 'import_calendar', entity_id='calendar.oud_dagboek')
    assert response == {'imported': 2, 'skipped': 1}
    assert state(hass, 'sensor.baby_feeding_next_bottle') == '14:00'
    assert not [data for _, data in pushes(phones) if data == REMINDER]
    with pytest.raises(ServiceValidationError, match='empty diary'):
        await call(hass, 'import_calendar', entity_id='calendar.oud_dagboek')


async def test_the_card_is_served_and_loaded_on_every_dashboard(hass: HomeAssistant, entry: MockConfigEntry, hass_client) -> None:  # noqa: ANN001
    client = await hass_client()
    response = await client.get('/baby_feeding/baby-feeding-card.js')
    assert response.status == 200
    assert 'baby-feeding-card' in await response.text()


async def test_only_one_entry_can_be_set_up(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    result = await hass.config_entries.flow.async_init(DOMAIN, context={'source': 'user'})
    assert result['type'] == 'abort'
    assert result['reason'] == 'single_instance_allowed'


async def test_set_up_through_the_user_interface(hass: HomeAssistant, phones: dict[str, list[ServiceCall]]) -> None:
    result = await hass.config_entries.flow.async_init(DOMAIN, context={'source': 'user'})
    assert result['type'] == 'form'
    result = await hass.config_entries.flow.async_configure(result['flow_id'], {'notify_services': PHONES, 'dashboard_url': DASHBOARD})
    assert result['type'] == 'create_entry'
    assert result['data'] == {'notify_services': PHONES, 'dashboard_url': DASHBOARD}
    assert result['title'] == 'Baby Feeding'


async def test_the_progress_sensor_moves_with_time(hass: HomeAssistant, entry: MockConfigEntry, freezer: FrozenDateTimeFactory) -> None:
    await call(hass, 'save_bottle', start='2026-11-14T12:30:00+01:00', amount=70)
    await advance(hass, freezer, to='2026-11-14T14:00:30')
    assert state(hass, 'sensor.baby_feeding_progress') == '50'


async def test_an_import_whose_planned_moment_passed_does_not_alert_again(hass: HomeAssistant, entry: MockConfigEntry, phones: dict[str, list[ServiceCall]], freezer: FrozenDateTimeFactory) -> None:
    async def get_events(service_call: ServiceCall) -> dict:
        return {'calendar.oud_dagboek': {'events': [{'summary': '70 cc', 'start': '2026-11-14T08:00:00+01:00', 'end': '2026-11-14T08:01:00+01:00'}]}}

    hass.services.async_register('calendar', 'get_events', get_events, supports_response='only')
    await call(hass, 'import_calendar', entity_id='calendar.oud_dagboek')
    await advance(hass, freezer, to='2026-11-14T12:45')
    assert state(hass, 'sensor.baby_feeding_next_bottle') == 'Now'
    assert not [data for _, data in pushes(phones) if data == REMINDER]


async def test_dutch_home_assistant_gets_dutch_texts_but_the_same_entity_ids(hass: HomeAssistant, entry: MockConfigEntry, phones: dict[str, list[ServiceCall]], freezer: FrozenDateTimeFactory) -> None:
    hass.config.language = 'nl'
    await call(hass, 'save_bottle', start='2026-11-14T11:12:00+01:00', amount=30)
    assert state(hass, 'sensor.baby_feeding_next_bottle') == '14:12'
    await advance(hass, freezer, to='2026-11-14T14:12:06')
    assert state(hass, 'sensor.baby_feeding_next_bottle') == 'Nu'
    reminders = [data for _, data in pushes(phones) if data.get('title') == 'Tijd voor de voeding']
    assert len(reminders) == 2
    events = await hass.services.async_call(
        'calendar', 'get_events', {'entity_id': 'calendar.baby_feeding_diary', 'start_date_time': local('2026-11-14T00:00'), 'end_date_time': local('2026-11-15T00:00')},
        blocking=True, return_response=True,
    )
    assert events['calendar.baby_feeding_diary']['events'][0]['summary'] == '30 cc'


async def test_a_refused_change_carries_a_translation_key(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    with pytest.raises(ServiceValidationError) as refused:
        await call(hass, 'save_bottle', start='2026-11-15T12:39:00+01:00', amount=30)
    assert (refused.value.translation_domain, refused.value.translation_key) == (DOMAIN, 'bottle_too_far_ahead')
