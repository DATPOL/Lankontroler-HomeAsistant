from dataclasses import dataclass
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry, ConfigEntryAuthFailed
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    ATTR_HW_VERSION,
    ATTR_SW_VERSION,
    CONF_MAC,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from tinytoolslib.exceptions import TinyToolsError, TinyToolsRequestUnauthenticated
from tinytoolslib.models import get_device

from .const import DOMAIN, LOGGER


@dataclass
class TinycontrolData:
    """Tinycontrol data."""

    model: str
    hardware_version: str
    software_version: str
    mac: str
    state: dict


class TinycontrolCoordinator(DataUpdateCoordinator[TinycontrolData]):

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.config_entry = entry
        self.client = get_device(
            entry.data[ATTR_HW_VERSION],
            entry.data[ATTR_SW_VERSION],
            host=entry.data[CONF_HOST],
            schema="https" if entry.data[CONF_PORT] == 443 else "http",
            port=entry.data[CONF_PORT],
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
            session=async_get_clientsession(hass),
        )
        if self.client is None:
            LOGGER.error(
                "TinycontrolCoordinator failed to create device client (%s)",
                entry.data[CONF_MAC],
            )
        super().__init__(
            hass,
            LOGGER,
            name=f"{DOMAIN}_{entry.data[CONF_MAC]}",
            update_interval=timedelta(seconds=entry.data[CONF_SCAN_INTERVAL]),
        )

    async def _async_update_data(self) -> TinycontrolData:
        try:
            data = await self.client.async_get_all()
            return TinycontrolData(
                model=self.client.info.model,
                hardware_version=data.get(
                    "hardware_version", self.client.hardware_version
                ),
                software_version=data.get(
                    "software_version", self.client.software_version
                ),
                mac=format_mac(data.get("mac")),
                state=data,
            )
        except TinyToolsRequestUnauthenticated as exc:
            raise ConfigEntryAuthFailed(
                f"Credentials expired for {self.client.host}:{self.client.port}"
            ) from exc
        except TinyToolsError as exc:
            raise UpdateFailed(exc) from exc
