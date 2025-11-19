"""Support for tinycontrol sensors."""

from dataclasses import dataclass
from typing import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    UnitOfReactivePower,
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfApparentPower,
    UnitOfPower,
    UnitOfPressure,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfTemperature,
    EntityCategory,
)
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import TinycontrolData, TinycontrolCoordinator
from .entity import TinycontrolEntity


@dataclass(frozen=True, kw_only=True)
class TinycontrolSensorEntityDescription(SensorEntityDescription):
    entity_category: str = EntityCategory.DIAGNOSTIC
    entity_registry_enabled_default: bool = False
    state_class: str = SensorStateClass.MEASUREMENT
    has_fn: Callable[[TinycontrolData], bool] = lambda _: True
    value_fn: Callable[[TinycontrolData], float | int | None]


SENSORS = [
    TinycontrolSensorEntityDescription(
        key="boardTemp",
        name="boardTemp",
        entity_registry_enabled_default=True,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        has_fn=lambda x: "boardTemp" in x.state,
        value_fn=lambda x: x.state["boardTemp"],
    ),
    TinycontrolSensorEntityDescription(
        key="boardHum",
        name="boardHum",
        entity_registry_enabled_default=True,
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=0,
        has_fn=lambda x: "boardHum" in x.state,
        value_fn=lambda x: x.state["boardHum"],
    ),
    TinycontrolSensorEntityDescription(
        key="boardVoltage",
        name="boardVoltage",
        entity_registry_enabled_default=True,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        suggested_display_precision=2,
        has_fn=lambda x: "boardVoltage" in x.state,
        value_fn=lambda x: x.state["boardVoltage"],
    ),
    *[
        TinycontrolSensorEntityDescription(
            key=f"ds{i}",
            name=f"DS{i}",
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            suggested_display_precision=1,
            has_fn=lambda x, _i=i: f"ds{_i}" in x.state,
            value_fn=lambda x, _i=i: x.state[f"ds{_i}"],
        )
        for i in range(1, 9)
    ],
    TinycontrolSensorEntityDescription(
        key="i2cTemp",
        name="i2cTemp (T1)",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        has_fn=lambda x: "i2cTemp" in x.state,
        value_fn=lambda x: x.state["i2cTemp"],
    ),
    TinycontrolSensorEntityDescription(
        key="i2cHum",
        name="i2cHum (H1)",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
        has_fn=lambda x: "i2cHum" in x.state,
        value_fn=lambda x: x.state["i2cHum"],
    ),
    TinycontrolSensorEntityDescription(
        key="i2cPressure",
        name="i2cPressure (P1)",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.HPA,
        suggested_display_precision=2,
        has_fn=lambda x: "i2cPressure" in x.state,
        value_fn=lambda x: x.state["i2cPressure"],
    ),
    TinycontrolSensorEntityDescription(
        key="pm1.0",
        name="PM1.0",
        device_class=SensorDeviceClass.PM1,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        suggested_display_precision=1,
        has_fn=lambda x: "pm1.0" in x.state,
        value_fn=lambda x: x.state["pm1.0"],
    ),
    TinycontrolSensorEntityDescription(
        key="pm2.5",
        name="PM2.5",
        device_class=SensorDeviceClass.PM25,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        suggested_display_precision=1,
        has_fn=lambda x: "pm2.5" in x.state,
        value_fn=lambda x: x.state["pm2.5"],
    ),
    TinycontrolSensorEntityDescription(
        key="pm4.0",
        name="PM4.0",
        # device_class=SensorDeviceClass.PM25, # No class for PM4.0
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        suggested_display_precision=1,
        has_fn=lambda x: "pm4.0" in x.state,
        value_fn=lambda x: x.state["pm4.0"],
    ),
    TinycontrolSensorEntityDescription(
        key="pm10.0",
        name="PM10.0",
        device_class=SensorDeviceClass.PM10,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        suggested_display_precision=1,
        has_fn=lambda x: "pm10.0" in x.state,
        value_fn=lambda x: x.state["pm10.0"],
    ),
    TinycontrolSensorEntityDescription(
        key="co2",
        name="CO2",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        suggested_display_precision=0,
        has_fn=lambda x: "co2" in x.state,
        value_fn=lambda x: x.state["co2"],
    ),
    # No device_class for diff as they can be temperature, voltage, power, energy, etc.
    *[
        TinycontrolSensorEntityDescription(
            key=f"diff{i}",
            name=f"DIFF{i}",
            suggested_display_precision=3,
            has_fn=lambda x, _i=i: f"diff{_i}" in x.state,
            value_fn=lambda x, _i=i: x.state[f"diff{_i}"],
        )
        for i in range(1, 7)
    ],
    *[
        TinycontrolSensorEntityDescription(
            key=f"iA{i}",
            name=f"iA{i}",
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            suggested_display_precision=2,
            has_fn=lambda x, _i=i: f"iAValue{_i}" in x.state,
            value_fn=lambda x, _i=i: x.state[f"iAValue{_i}"],
        )
        for i in range(1, 9)
    ],
    *[
        TinycontrolSensorEntityDescription(
            key=f"power{i}",
            name=f"POWER{i}",
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.KILO_WATT,
            suggested_display_precision=3,
            has_fn=lambda x, _i=i: f"power{_i}" in x.state,
            value_fn=lambda x, _i=i: x.state[f"power{_i}"],
        )
        for i in range(1, 7)
    ],
    *[
        TinycontrolSensorEntityDescription(
            key=f"energy{i}",
            name=f"ENERGY{i}",
            state_class=SensorStateClass.TOTAL,
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            suggested_display_precision=3,
            has_fn=lambda x, _i=i: f"energy{_i}" in x.state,
            value_fn=lambda x, _i=i: x.state[f"energy{_i}"],
        )
        for i in range(1, 7)
    ],
    # No device_class for mX as they can be anything.
    *[
        TinycontrolSensorEntityDescription(
            key=f"mValue{i}",
            name=f"Custom reading m{i}",
            state_class=None,  # It may be measurement or total
            has_fn=lambda x, _i=i: f"mValue{_i}" in x.state,
            value_fn=lambda x, _i=i: x.state[f"mValue{_i}"],
        )
        for i in range(1, 31)
    ],
    # Only for tcPDU
    TinycontrolSensorEntityDescription(
        key="uRms",
        name="U RMS",
        entity_registry_enabled_default=True,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        suggested_display_precision=1,
        has_fn=lambda x: "uRms" in x.state,
        value_fn=lambda x: x.state["uRms"],
    ),
    TinycontrolSensorEntityDescription(
        key="iRms",
        name="I RMS",
        entity_registry_enabled_default=True,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        suggested_display_precision=2,
        has_fn=lambda x: "iRms" in x.state,
        value_fn=lambda x: x.state["iRms"],
    ),
    TinycontrolSensorEntityDescription(
        key="pActive",
        name="Power active",
        entity_registry_enabled_default=True,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        suggested_display_precision=3,
        has_fn=lambda x: "pActive" in x.state,
        value_fn=lambda x: x.state["pActive"],
    ),
    TinycontrolSensorEntityDescription(
        key="pReactive",
        name="Power reactive",
        entity_registry_enabled_default=True,
        device_class=SensorDeviceClass.REACTIVE_POWER,
        native_unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
        suggested_display_precision=3,
        has_fn=lambda x: "pReactive" in x.state,
        value_fn=lambda x: x.state["pReactive"],
    ),
    TinycontrolSensorEntityDescription(
        key="pApparent",
        name="Power apparent",
        device_class=SensorDeviceClass.APPARENT_POWER,
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        suggested_display_precision=3,
        has_fn=lambda x: "pApparent" in x.state,
        value_fn=lambda x: x.state["pApparent"],
    ),
    TinycontrolSensorEntityDescription(
        key="pFactor",
        name="Power factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=None,
        suggested_display_precision=2,
        has_fn=lambda x: "pFactor" in x.state,
        value_fn=lambda x: x.state["pFactor"],
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up tinycontrol sensor based on a config entry."""
    coordinator: TinycontrolCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        TinycontrolSensorEntity(
            coordinator=coordinator,
            description=description,
        )
        for description in SENSORS
        if description.has_fn(coordinator.data)
    )


class TinycontrolSensorEntity(TinycontrolEntity, SensorEntity):
    """TinycontrolSensorEntity."""

    entity_description: TinycontrolSensorEntityDescription

    def __init__(
        self,
        coordinator: TinycontrolCoordinator,
        description: TinycontrolSensorEntityDescription,
    ) -> None:
        """Initiate tinycontrol sensor."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.mac}_{description.key}"

    @property
    def native_value(self) -> float | int | None:
        """Return the sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)
