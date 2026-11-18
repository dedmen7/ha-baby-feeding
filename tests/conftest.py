"""Shared fixtures: a Home Assistant in Amsterdam time with two phones and the integration set up."""

from collections.abc import AsyncGenerator
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant, ServiceCall
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_mock_service

from custom_components.baby_feeding.const import CONF_DASHBOARD_URL, CONF_NOTIFY_SERVICES, DOMAIN

AMSTERDAM = ZoneInfo('Europe/Amsterdam')
PHONES = ['notify.mobile_app_telefoon_a', 'notify.mobile_app_telefoon_b']
DASHBOARD = '/dashboard-main/voeding'


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    return None


def local(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=AMSTERDAM)


@pytest.fixture
async def phones(hass: HomeAssistant) -> dict[str, list[ServiceCall]]:
    await hass.config.async_set_time_zone('Europe/Amsterdam')
    return {phone: async_mock_service(hass, 'notify', phone.split('.')[1]) for phone in PHONES}


def pushes(phones: dict[str, list[ServiceCall]]) -> list[tuple[str, dict]]:
    """Every push sent so far, per phone, in the order each phone received them."""
    return [(phone, dict(call.data)) for phone, calls in phones.items() for call in calls]


@pytest.fixture
async def entry(hass: HomeAssistant, phones: dict[str, list[ServiceCall]], freezer: FrozenDateTimeFactory) -> AsyncGenerator[MockConfigEntry]:
    freezer.move_to(local('2026-11-14T12:38'))
    config_entry = MockConfigEntry(domain=DOMAIN, title='Babyvoeding', data={CONF_NOTIFY_SERVICES: PHONES, CONF_DASHBOARD_URL: DASHBOARD})
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    yield config_entry
