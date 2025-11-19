"""Config flow to configure the tinycontrol integration."""

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    SOURCE_REAUTH,
    SOURCE_RECONFIGURE,
    SOURCE_USER,
    ConfigFlow,
    FlowCancelledError,
)
from homeassistant.const import (
    ATTR_HW_VERSION,
    ATTR_SW_VERSION,
    CONF_HOST,
    CONF_MAC,
    CONF_MODEL,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import format_mac
from tinytoolslib.exceptions import TinyToolsError, TinyToolsRequestUnauthenticated
from tinytoolslib.models import async_get_version

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN


class TinycontrolFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle config flows for a tinycontrol device."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        if user_input is None:
            return self._async_show_setup_form()
        entry_data = {**user_input}
        return await self._async_step(entry_data)

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle a reconfigure flow."""
        entry = self._get_reconfigure_entry()
        if user_input is None:
            return self._async_show_setup_form(entry.data)
        entry_data = {**entry.data, **user_input}
        return await self._async_step(entry_data)

    async def async_step_reauth(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the re-authentication step."""
        entry = self._get_reauth_entry()
        if user_input is None:
            return self._async_show_setup_form(entry.data)
        entry_data = {**entry.data, **user_input}
        return await self._async_step(entry_data)

    async def _async_step(self, entry_data: dict[str, Any]):
        """Handle step for user/reauth/reconfigure flows."""
        errors = {}
        try:
            entry_data = await self._get_device_info(entry_data)
        except TinyToolsRequestUnauthenticated:
            errors[CONF_USERNAME] = "wrong_credentials"
            errors[CONF_PASSWORD] = "wrong_credentials"
        except TinyToolsError:
            errors["base"] = "cannot_connect"
        if errors:
            return self._async_show_setup_form(entry_data, errors)
        return await self._async_create_entry(entry_data)

    @callback
    def _async_show_setup_form(
        self,
        entry_data: dict[str, Any] | None = None,
        errors: dict[str, str] | None = None,
    ) -> FlowResult:
        """Show the setup form to the user."""
        entry_data = entry_data or {}
        # Data schemas should be handled dynamically due to default/initial values, eg. for reauth/reconfigure.
        if self.source == SOURCE_USER or self.source == SOURCE_RECONFIGURE:
            data_schema = vol.Schema(
                {
                    vol.Required(CONF_HOST, default=entry_data.get(CONF_HOST, "")): str,
                    vol.Optional(CONF_PORT, default=entry_data.get(CONF_PORT, 80)): int,
                    vol.Optional(
                        CONF_USERNAME, default=entry_data.get(CONF_USERNAME, "")
                    ): str,
                    vol.Optional(
                        CONF_PASSWORD, default=entry_data.get(CONF_PASSWORD, "")
                    ): str,
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=entry_data.get(
                            CONF_SCAN_INTERVAL,
                            int(DEFAULT_SCAN_INTERVAL.total_seconds()),
                        ),
                    ): vol.All(int, vol.Range(min=1)),
                }
            )
        elif self.source == SOURCE_REAUTH:
            data_schema = vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME, default=entry_data.get(CONF_USERNAME, "")
                    ): str,
                    vol.Required(
                        CONF_PASSWORD, default=entry_data.get(CONF_PASSWORD, "")
                    ): str,
                }
            )
        else:
            raise FlowCancelledError(f"No data schema for current flow {self.source}")
        return self.async_show_form(
            step_id=self.source,
            data_schema=data_schema,
            errors=errors or {},
        )

    async def _async_create_entry(self, entry_data: dict[str, Any]) -> FlowResult:
        """Create a config entry or update existing one for reauth/reconfigure."""
        await self.async_set_unique_id(entry_data[CONF_MAC])
        if self.source == SOURCE_REAUTH or self.source == SOURCE_RECONFIGURE:
            self._abort_if_unique_id_mismatch()
            if self.source == SOURCE_REAUTH:
                entry = self._get_reauth_entry()
            else:  # self.source == SOURCE_RECONFIGURE:
                entry = self._get_reconfigure_entry()
            return self.async_update_reload_and_abort(entry, data_updates=entry_data)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=f"{entry_data[CONF_MODEL]} ({entry_data[CONF_MAC]}, {entry_data[CONF_HOST]}:{entry_data[CONF_PORT]})",
            data=entry_data,
        )

    async def _get_device_info(self, entry_data: dict[str, Any]) -> None:
        """Get device information from a Tinycontrol device."""
        session = async_get_clientsession(self.hass)
        version_info = await async_get_version(
            entry_data[CONF_HOST],
            entry_data[CONF_PORT],
            'http', # For now use hardcoded protocol
            entry_data[CONF_USERNAME],
            entry_data[CONF_PASSWORD],
            with_device=True,
            silent=False,
            session=session,
        )
        tiny_device = version_info["device_model"]
        data = await tiny_device.async_get_all()
        # Return device data
        return {
            CONF_MODEL: tiny_device.info.model,
            CONF_HOST: entry_data[CONF_HOST],
            CONF_PORT: tiny_device.port,
            CONF_USERNAME: entry_data[CONF_USERNAME],
            CONF_PASSWORD: entry_data[CONF_PASSWORD],
            CONF_MAC: format_mac(data["mac"]),
            ATTR_HW_VERSION: version_info["hardware_version"],
            ATTR_SW_VERSION: version_info["software_version"],
            CONF_SCAN_INTERVAL: entry_data[CONF_SCAN_INTERVAL],
        }
