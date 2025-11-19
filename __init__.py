"""Support for tinycontrol devices."""

from copy import deepcopy

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, ATTR_SW_VERSION, CONF_MAC
from homeassistant.core import HomeAssistant

from .const import DOMAIN, LOGGER
from .coordinator import TinycontrolCoordinator
from .services import async_setup_services, async_unload_services

PLATFORMS = [Platform.SENSOR, Platform.SWITCH, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up tinycontrol device from a config entry."""
    coordinator = TinycontrolCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    # Update config entry because of SW change.
    if coordinator.data.software_version != entry.data[ATTR_SW_VERSION]:
        LOGGER.info(
            "Updating config entry for %s due to SW change (%s -> %s)",
            entry.data[CONF_MAC],
            entry.data[ATTR_SW_VERSION],
            coordinator.data.software_version,
        )
        coordinator.client.software_version = coordinator.data.software_version
        new_data = deepcopy(dict(entry.data))
        new_data[ATTR_SW_VERSION] = coordinator.data.software_version
        hass.config_entries.async_update_entry(entry, data=new_data)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await async_setup_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload tinycontrol device config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        del hass.data[DOMAIN][entry.entry_id]
    await async_unload_services(hass, unload_ok)
    return unload_ok
