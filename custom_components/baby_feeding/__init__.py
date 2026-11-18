"""Baby Feeding: bottle diary, feeding rhythm, reminders and the dashboard card."""

import hashlib
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import voluptuous as vol
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util

from .const import CARD_FILENAME, CARD_URL_PATH, DOMAIN
from .diary import FeedError, FeedingState
from .manager import FeedingManager

PLATFORMS = [Platform.SENSOR, Platform.CALENDAR]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
AMOUNT = vol.All(vol.Coerce(int), vol.Range(min=0, max=9999))
FEED_SCHEMA = vol.Schema({vol.Required('start'): cv.datetime, vol.Required('amount'): AMOUNT})
CARD_FILE = Path(__file__).parent / 'frontend' / CARD_FILENAME

type BabyFeedingConfigEntry = ConfigEntry[FeedingManager]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    card_url = CARD_URL_PATH + '/' + CARD_FILENAME
    await hass.http.async_register_static_paths([StaticPathConfig(url_path=card_url, path=str(CARD_FILE), cache_headers=False)])
    if 'frontend' in hass.config.components:
        module_url = await hass.async_add_executor_job(card_module_url, CARD_FILE)
        add_extra_js_url(hass=hass, url=module_url)
    _register_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: BabyFeedingConfigEntry) -> bool:
    manager = FeedingManager.from_entry_data(hass, {**entry.data, **entry.options})
    await manager.async_start()
    entry.runtime_data = manager
    entry.async_on_unload(manager.async_stop)
    entry.async_on_unload(entry.add_update_listener(_async_reload))
    await hass.config_entries.async_forward_entry_setups(entry=entry, platforms=PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: BabyFeedingConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry=entry, platforms=PLATFORMS)


async def _async_reload(hass: HomeAssistant, entry: BabyFeedingConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


def _register_services(hass: HomeAssistant) -> None:
    def manager() -> FeedingManager:
        entries = hass.config_entries.async_loaded_entries(DOMAIN)
        if not entries:
            raise ServiceValidationError('Baby Feeding is not loaded.', translation_domain=DOMAIN, translation_key='not_loaded')
        return entries[0].runtime_data

    def register(name: str, schema: vol.Schema, run: Callable[[FeedingManager, dict[str, Any]], Awaitable[Any]]) -> None:
        async def handle(call: ServiceCall) -> ServiceResponse:
            try:
                result = await run(manager(), dict(call.data))
            except FeedError as error:
                raise ServiceValidationError(str(error), translation_domain=DOMAIN, translation_key=error.key) from error
            return result if isinstance(result, dict) else _summary(result)

        hass.services.async_register(domain=DOMAIN, service=name, service_func=handle, schema=schema, supports_response=SupportsResponse.OPTIONAL)

    register('save_bottle', FEED_SCHEMA, lambda target, data: target.async_save_bottle(start=data['start'], amount=data['amount']))
    register('add_earlier_feed', FEED_SCHEMA, lambda target, data: target.async_add_earlier_feed(start=data['start'], amount=data['amount']))
    register(
        'update_feed', FEED_SCHEMA.extend({vol.Required('feed_id'): cv.string}),
        lambda target, data: target.async_update_feed(feed_id=data['feed_id'], start=data['start'], amount=data['amount']),
    )
    register('delete_feed', vol.Schema({vol.Required('feed_id'): cv.string}), lambda target, data: target.async_delete_feed(feed_id=data['feed_id']))
    register('new_bottle', vol.Schema({}), lambda target, data: target.async_new_bottle())
    register(
        'set_settings',
        vol.Schema({
            vol.Required('standard_amount'): AMOUNT,
            vol.Optional('maximum_amount'): vol.Any(None, AMOUNT),
            vol.Required('night_custom_enabled'): cv.boolean,
            vol.Required('night_hours'): vol.All(vol.Coerce(int), vol.Range(min=3, max=8)),
        }),
        lambda target, data: target.async_set_settings(
            standard_amount=data['standard_amount'], maximum_amount=data.get('maximum_amount'),
            night_custom_enabled=data['night_custom_enabled'], night_hours=data['night_hours'],
        ),
    )
    register('import_calendar', vol.Schema({vol.Required('entity_id'): cv.entity_id}), lambda target, data: target.async_import_calendar(entity_id=data['entity_id']))


def card_module_url(card_file: Path) -> str:
    """The card URL with a content hash, so browsers and the phone apps load a new card after every update."""
    version = hashlib.sha256(card_file.read_bytes()).hexdigest()[:12]
    return CARD_URL_PATH + '/' + CARD_FILENAME + '?v=' + version


def _summary(state: FeedingState) -> dict[str, Any]:
    plan = state.plan
    return {
        'next_due': None if plan is None else dt_util.as_local(plan.due).isoformat(),
        'plan_feed_id': None if plan is None else plan.feed_id,
        'open_start': None if state.pending is None else dt_util.as_local(state.pending).isoformat(),
    }
