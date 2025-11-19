"""Support for tinycontrol binary sensors."""

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import TinycontrolData, TinycontrolCoordinator
from .entity import TinycontrolEntity


@dataclass(frozen=True, kw_only=True)
class TinycontrolBinarySensorEntityDescription(BinarySensorEntityDescription):
    entity_registry_enabled_default: bool = False
    has_fn: Callable[[TinycontrolData], bool] = lambda _: True
    is_on_fn: Callable[[TinycontrolData], bool | None]


BINARY_SENSORS = [
    *[
        TinycontrolBinarySensorEntityDescription(
            key=f"id{i}",
            name=f"iD{i}",
            # device_class can be set by the user depending on their use case
            entity_category=EntityCategory.DIAGNOSTIC,
            has_fn=lambda x, _i=i: f"iDValue{_i}" in x.state,
            is_on_fn=lambda x, _i=i: x.state[f"iDValue{_i}"],
        )
        for i in range(1, 5)
    ],
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up tinycontrol device binary sensor based on a config entry."""
    coordinator: TinycontrolCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        TinycontrolBinarySensorEntity(
            coordinator=coordinator,
            description=description,
        )
        for description in BINARY_SENSORS
        if description.has_fn(coordinator.data)
    )


class TinycontrolBinarySensorEntity(TinycontrolEntity, BinarySensorEntity):
    """TinycontrolBinarySensorEntity."""

    entity_description: TinycontrolBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: TinycontrolCoordinator,
        description: TinycontrolBinarySensorEntityDescription,
    ) -> None:
        """Initialize tinycontrol device sensor."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.mac}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return state of the binary sensor."""
        return self.entity_description.is_on_fn(self.coordinator.data)
