"""Support for tinycontrol switches."""

from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Any, Callable


from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
    SwitchDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from tinytoolslib.models import DeviceModel

from .const import DOMAIN
from .coordinator import TinycontrolData, TinycontrolCoordinator, TinyToolsError
from .entity import TinycontrolEntity


@dataclass(frozen=True, kw_only=True)
class TinycontrolSwitchEntityDescription(SwitchEntityDescription):
    """Class describing Tinycontrol switch entities."""

    entity_registry_enabled_default: bool = False
    has_fn: Callable[[TinycontrolData], bool] = lambda _: True
    is_on_fn: Callable[[TinycontrolData], bool | None]
    set_fn: Callable[[DeviceModel, bool], Awaitable[Any]]


SWITCHES = [
    *[
        TinycontrolSwitchEntityDescription(
            key=f"out{i}",
            name=f"OUT{i}",
            device_class=SwitchDeviceClass.SWITCH,
            has_fn=lambda x, _i=i: f"out{_i}" in x.state,
            is_on_fn=lambda x, _i=i: x.state[f"out{_i}"],
            set_fn=lambda client, on, _i=i: client.async_set_out(_i, on),
        )
        for i in range(0, 8)
    ],
    *[
        TinycontrolSwitchEntityDescription(
            key=f"pwm{i}",
            name=f"PWM{i}",
            device_class=SwitchDeviceClass.SWITCH,
            has_fn=lambda x, _i=i: f"pwm{_i}" in x.state,
            is_on_fn=lambda x, _i=i: x.state[f"pwm{_i}"],
            set_fn=lambda client, on, _i=i: client.async_set_pwm(_i, on),
        )
        for i in range(0, 4)
    ],
    *[
        TinycontrolSwitchEntityDescription(
            key=f"event{i}",
            name=f"EVENT{i}",
            device_class=SwitchDeviceClass.SWITCH,
            has_fn=lambda x, _i=i: f"event{_i}" in x.state,
            is_on_fn=lambda x, _i=i: x.state[f"event{_i}"],
            set_fn=lambda client, on, _i=i: client.async_set_var(_i, on),
        )
        for i in range(1, 9)
    ],
    *[
        TinycontrolSwitchEntityDescription(
            key=f"var{i}",
            name=f"VAR{i}",
            device_class=SwitchDeviceClass.SWITCH,
            has_fn=lambda x, _i=i: f"var{_i}" in x.state,
            is_on_fn=lambda x, _i=i: x.state[f"var{_i}"],
            set_fn=lambda client, on, _i=i: client.async_set_var(_i, on),
        )
        for i in range(1, 9)
    ],
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up tinycontrol switch based on a config entry."""
    coordinator: TinycontrolCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        TinycontrolSwitchEntity(
            coordinator=coordinator,
            description=description,
        )
        for description in SWITCHES
        if description.has_fn(coordinator.data)
    )


class TinycontrolSwitchEntity(TinycontrolEntity, SwitchEntity):
    """Defines a tinycontrol switch."""

    entity_description: TinycontrolSwitchEntityDescription

    def __init__(
        self,
        coordinator: TinycontrolCoordinator,
        description: TinycontrolSwitchEntityDescription,
    ) -> None:
        """Initiate tinycontrol switch."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.mac}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return state of the switch."""
        return self.entity_description.is_on_fn(self.coordinator.data)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        try:
            await self.entity_description.set_fn(self.coordinator.client, 1)
        except TinyToolsError as error:
            raise HomeAssistantError(
                "An error occurred while updating the tinycontrol"
            ) from error
        finally:
            await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        try:
            await self.entity_description.set_fn(self.coordinator.client, 0)
        except TinyToolsError as error:
            raise HomeAssistantError(
                "An error occurred while updating the tinycontrol"
            ) from error
        finally:
            await self.coordinator.async_refresh()
