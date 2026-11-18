"""Setup in the user interface: which phones get reminders and which dashboard they open."""

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector

from .const import CONF_DASHBOARD_URL, CONF_NOTIFY_SERVICES, DEFAULT_DASHBOARD_URL, DOMAIN


def _schema(hass: HomeAssistant, defaults: dict[str, Any]) -> vol.Schema:
    phones = sorted('notify.' + name for name in hass.services.async_services_for_domain('notify') if name.startswith('mobile_app_'))
    return vol.Schema({
        vol.Required(CONF_NOTIFY_SERVICES, default=defaults.get(CONF_NOTIFY_SERVICES, [])): selector.SelectSelector(
            selector.SelectSelectorConfig(options=phones, multiple=True, custom_value=True),
        ),
        vol.Required(CONF_DASHBOARD_URL, default=defaults.get(CONF_DASHBOARD_URL, DEFAULT_DASHBOARD_URL)): selector.TextSelector(),
    })


def _valid(user_input: dict[str, Any]) -> dict[str, str]:
    errors = {}
    if not str(user_input[CONF_DASHBOARD_URL]).startswith('/') or str(user_input[CONF_DASHBOARD_URL]).startswith('//'):
        errors[CONF_DASHBOARD_URL] = 'invalid_dashboard_url'
    if not all(str(service).startswith('notify.') for service in user_input[CONF_NOTIFY_SERVICES]):
        errors[CONF_NOTIFY_SERVICES] = 'invalid_notify_service'
    return errors


class BabyFeedingConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            errors = _valid(user_input)
            if not errors:
                return self.async_create_entry(title='Baby Feeding', data=user_input)
        return self.async_show_form(step_id='user', data_schema=_schema(self.hass, user_input or {}), errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return BabyFeedingOptionsFlow()


class BabyFeedingOptionsFlow(OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            errors = _valid(user_input)
            if not errors:
                return self.async_create_entry(data=user_input)
        defaults = user_input or {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(step_id='init', data_schema=_schema(self.hass, defaults), errors=errors)
