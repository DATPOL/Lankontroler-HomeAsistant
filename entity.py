"""Base entity for tinycontrol integration."""

from homeassistant.const import CONF_MAC, ATTR_CONNECTIONS
from homeassistant.helpers.device_registry import (
    CONNECTION_NETWORK_MAC,
    DeviceInfo,
    format_mac,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TinycontrolCoordinator


class TinycontrolEntity(CoordinatorEntity[TinycontrolCoordinator]):
    """Defines a base tinycontrol entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: TinycontrolCoordinator) -> None:
        """Initialize the tinycontrol entity."""
        super().__init__(coordinator=coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.data.mac)},
            manufacturer="tinycontrol",
            model=coordinator.data.model,
            sw_version=coordinator.data.software_version,
            hw_version=coordinator.data.hardware_version,
        )
        if (mac := coordinator.config_entry.data.get(CONF_MAC)) is not None:
            self._attr_device_info[ATTR_CONNECTIONS] = {
                (CONNECTION_NETWORK_MAC, format_mac(mac))
            }
