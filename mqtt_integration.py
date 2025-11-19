"""Module for generating configuration for home-assistant MQTT integration.

It (generate_config()) generates list of dicts with entries for components
(sensor, switch, binary_sensor).

It can be tested manually:

```py
params = {'args': ["LK4LTE", "LK HW 4.0", "E8:6B:11:11:11:11", "4.0", "1.37", "xxxxxx/x/x2"], 'kwargs': {'series': ['boardVoltage', 'OUT1', 'Custom reading m1']}}
# Print configuration in JSON format:
print(json.dumps(generate_config(*config['args'], **config['kwargs']), indent=2))
```

TODO: Allow generating config by passing address of LK, so it would read
MQTT client options and other parameters needed for generate_config().
"""

import re
from copy import deepcopy

from homeassistant.const import Platform
from tinytoolslib.models import LK_HW_40

from .sensor import SENSORS


# Entity/component types
SENSOR = Platform.SENSOR
BINARY_SENSOR = Platform.BINARY_SENSOR
SWITCH = Platform.SWITCH


# region LK4 specific functions for generating entity configs (assigned in SERIES)
def get_lk4_out_options(serie, device):
    """Get options for LK4 OUT entity."""
    index = serie["name"][-1]
    return {
        "command_topic": f"{device['prefix']}/cmd",
        "payload_on": f"out{index}=1",
        "payload_off": f"out{index}=0",
    }


def get_lk4_pwm_options(serie, device):
    """Get options for LK4 PWM entity."""
    index = serie["name"][-1]
    return {
        "command_topic": f"{device['prefix']}/cmd",
        "payload_on": f"pwm{index}=1",
        "payload_off": f"pwm{index}=0",
    }


def get_lk4_var_options(serie, device):
    """Get options for LK4 VAR entity."""
    index = serie["name"][-1]
    return {
        "command_topic": f"{device['prefix']}/cmd",
        "payload_on": f"var{index}=1",
        "payload_off": f"var{index}=0",
    }


# endregion


# entity/component field defines how serie will be loaded in HA MQTT integration
LK4_MODEL = LK_HW_40.info.model
LK4_SERIES = [
    {"topic": "boardVoltage", "name": "boardVoltage", "map_to": 0, "entity": SENSOR},
    {"topic": "boardTemp", "name": "boardTemp", "map_to": 1, "entity": SENSOR},
    {"topic": "boardHum", "name": "boardHum", "map_to": 2, "entity": SENSOR},
    {"topic": "iAValue1", "name": "iA1", "map_to": 3, "entity": SENSOR},
    {"topic": "iAValue2", "name": "iA2", "map_to": 4, "entity": SENSOR},
    {"topic": "iAValue3", "name": "iA3", "map_to": 5, "entity": SENSOR},
    {"topic": "ds1", "name": "DS1", "map_to": 6, "entity": SENSOR},
    {"topic": "ds2", "name": "DS2", "map_to": 7, "entity": SENSOR},
    {"topic": "ds3", "name": "DS3", "map_to": 8, "entity": SENSOR},
    {"topic": "ds4", "name": "DS4", "map_to": 9, "entity": SENSOR},
    {"topic": "ds5", "name": "DS5", "map_to": 10, "entity": SENSOR},
    {"topic": "ds6", "name": "DS6", "map_to": 11, "entity": SENSOR},
    {"topic": "ds7", "name": "DS7", "map_to": 12, "entity": SENSOR},
    {"topic": "ds8", "name": "DS8", "map_to": 13, "entity": SENSOR},
    {"topic": "i2cTemp", "name": "i2cTemp (T1)", "map_to": 14, "entity": SENSOR},
    {"topic": "i2cHum", "name": "i2cHum (H1)", "map_to": 15, "entity": SENSOR},
    {
        "topic": "i2cPressure",
        "name": "i2cPressure (P1)",
        "map_to": 16,
        "entity": SENSOR,
    },
    {"topic": "diff1", "name": "DIFF1", "map_to": 17, "entity": SENSOR},
    {"topic": "diff2", "name": "DIFF2", "map_to": 18, "entity": SENSOR},
    {"topic": "diff3", "name": "DIFF3", "map_to": 19, "entity": SENSOR},
    {"topic": "diff4", "name": "DIFF4", "map_to": 20, "entity": SENSOR},
    {"topic": "diff5", "name": "DIFF5", "map_to": 21, "entity": SENSOR},
    {"topic": "diff6", "name": "DIFF6", "map_to": 22, "entity": SENSOR},
    {"topic": "iDValue1", "name": "INPD1", "map_to": 23, "entity": BINARY_SENSOR},
    {"topic": "iDValue2", "name": "INPD2", "map_to": 24, "entity": BINARY_SENSOR},
    {"topic": "iDValue3", "name": "INPD3", "map_to": 25, "entity": BINARY_SENSOR},
    {"topic": "iDValue4", "name": "INPD4", "map_to": 26, "entity": BINARY_SENSOR},
    {
        "topic": "out1",
        "name": "OUT1",
        "map_to": 27,
        "entity": SWITCH,
        "opt_func": get_lk4_out_options,
    },
    {
        "topic": "out2",
        "name": "OUT2",
        "map_to": 28,
        "entity": SWITCH,
        "opt_func": get_lk4_out_options,
    },
    {
        "topic": "out3",
        "name": "OUT3",
        "map_to": 29,
        "entity": SWITCH,
        "opt_func": get_lk4_out_options,
    },
    {
        "topic": "out4",
        "name": "OUT4",
        "map_to": 30,
        "entity": SWITCH,
        "opt_func": get_lk4_out_options,
    },
    {
        "topic": "out5",
        "name": "OUT5",
        "map_to": 31,
        "entity": SWITCH,
        "opt_func": get_lk4_out_options,
    },
    {
        "topic": "out6",
        "name": "OUT6",
        "map_to": 32,
        "entity": SWITCH,
        "opt_func": get_lk4_out_options,
    },
    {
        "topic": "pwm1",
        "name": "PWM1",
        "map_to": 33,
        "entity": SWITCH,
        "opt_func": get_lk4_pwm_options,
    },
    {
        "topic": "pwm2",
        "name": "PWM2",
        "map_to": 34,
        "entity": SWITCH,
        "opt_func": get_lk4_pwm_options,
    },
    {
        "topic": "pwm3",
        "name": "PWM3",
        "map_to": 35,
        "entity": SWITCH,
        "opt_func": get_lk4_pwm_options,
    },
    {"topic": "pwmDuty1", "name": "PWM1 Duty", "map_to": 36, "entity": SENSOR},
    {"topic": "pwmDuty2", "name": "PWM2 Duty", "map_to": 37, "entity": SENSOR},
    {"topic": "pwmDuty3", "name": "PWM3 Duty", "map_to": 38, "entity": SENSOR},
    {"topic": "power1", "name": "POWER1", "map_to": 39, "entity": SENSOR},
    {"topic": "power2", "name": "POWER2", "map_to": 40, "entity": SENSOR},
    {"topic": "power3", "name": "POWER3", "map_to": 41, "entity": SENSOR},
    {"topic": "power4", "name": "POWER4", "map_to": 42, "entity": SENSOR},
    {"topic": "power5", "name": "POWER5", "map_to": 43, "entity": SENSOR},
    {"topic": "power6", "name": "POWER6", "map_to": 44, "entity": SENSOR},
    {"topic": "energy1", "name": "ENERGY1", "map_to": 45, "entity": SENSOR},
    {"topic": "energy2", "name": "ENERGY2", "map_to": 46, "entity": SENSOR},
    {"topic": "energy3", "name": "ENERGY3", "map_to": 47, "entity": SENSOR},
    {"topic": "energy4", "name": "ENERGY4", "map_to": 48, "entity": SENSOR},
    {"topic": "energy5", "name": "ENERGY5", "map_to": 49, "entity": SENSOR},
    {"topic": "energy6", "name": "ENERGY6", "map_to": 50, "entity": SENSOR},
    {
        "topic": "var1",
        "name": "VAR1",
        "map_to": 51,
        "entity": SWITCH,
        "opt_func": get_lk4_var_options,
    },
    {
        "topic": "var2",
        "name": "VAR2",
        "map_to": 52,
        "entity": SWITCH,
        "opt_func": get_lk4_var_options,
    },
    {
        "topic": "var3",
        "name": "VAR3",
        "map_to": 53,
        "entity": SWITCH,
        "opt_func": get_lk4_var_options,
    },
    {
        "topic": "var4",
        "name": "VAR4",
        "map_to": 54,
        "entity": SWITCH,
        "opt_func": get_lk4_var_options,
    },
    {
        "topic": "var5",
        "name": "VAR5",
        "map_to": 55,
        "entity": SWITCH,
        "opt_func": get_lk4_var_options,
    },
    {
        "topic": "var6",
        "name": "VAR6",
        "map_to": 56,
        "entity": SWITCH,
        "opt_func": get_lk4_var_options,
    },
    {
        "topic": "var7",
        "name": "VAR7",
        "map_to": 57,
        "entity": SWITCH,
        "opt_func": get_lk4_var_options,
    },
    {
        "topic": "var8",
        "name": "VAR8",
        "map_to": 58,
        "entity": SWITCH,
        "opt_func": get_lk4_var_options,
    },
    {"topic": "pm1", "name": "PM1.0", "map_to": 59, "entity": SENSOR},
    {"topic": "pm2", "name": "PM2.5", "map_to": 60, "entity": SENSOR},
    {"topic": "pm4", "name": "PM4.0", "map_to": 61, "entity": SENSOR},
    {"topic": "pm10", "name": "PM10.0", "map_to": 62, "entity": SENSOR},
    {"topic": "co2", "name": "CO2", "map_to": 63, "entity": SENSOR},
    # { 'topic': 'distance', 'name': 'Distance sensor', 'map_to': 64, 'entity': SENSOR },
    # { 'topic': 'i2cAirQuality', 'name': 'IAQ', 'map_to': 65, 'entity': SENSOR },
    {"topic": "m1", "name": "Custom reading m1", "map_to": 66, "entity": SENSOR},
    {"topic": "m2", "name": "Custom reading m2", "map_to": 67, "entity": SENSOR},
    {"topic": "m3", "name": "Custom reading m3", "map_to": 68, "entity": SENSOR},
    {"topic": "m4", "name": "Custom reading m4", "map_to": 69, "entity": SENSOR},
    {"topic": "m5", "name": "Custom reading m5", "map_to": 70, "entity": SENSOR},
    {"topic": "m6", "name": "Custom reading m6", "map_to": 71, "entity": SENSOR},
    {"topic": "m7", "name": "Custom reading m7", "map_to": 72, "entity": SENSOR},
    {"topic": "m8", "name": "Custom reading m8", "map_to": 73, "entity": SENSOR},
    {"topic": "m9", "name": "Custom reading m9", "map_to": 74, "entity": SENSOR},
    {"topic": "m10", "name": "Custom reading m10", "map_to": 75, "entity": SENSOR},
    {"topic": "m11", "name": "Custom reading m11", "map_to": 76, "entity": SENSOR},
    {"topic": "m12", "name": "Custom reading m12", "map_to": 77, "entity": SENSOR},
    {"topic": "m13", "name": "Custom reading m13", "map_to": 78, "entity": SENSOR},
    {"topic": "m14", "name": "Custom reading m14", "map_to": 79, "entity": SENSOR},
    {"topic": "m15", "name": "Custom reading m15", "map_to": 80, "entity": SENSOR},
    {"topic": "m16", "name": "Custom reading m16", "map_to": 81, "entity": SENSOR},
    {"topic": "m17", "name": "Custom reading m17", "map_to": 82, "entity": SENSOR},
    {"topic": "m18", "name": "Custom reading m18", "map_to": 83, "entity": SENSOR},
    {"topic": "m19", "name": "Custom reading m19", "map_to": 84, "entity": SENSOR},
    {"topic": "m20", "name": "Custom reading m20", "map_to": 85, "entity": SENSOR},
    {"topic": "m21", "name": "Custom reading m21", "map_to": 86, "entity": SENSOR},
    {"topic": "m22", "name": "Custom reading m22", "map_to": 87, "entity": SENSOR},
    {"topic": "m23", "name": "Custom reading m23", "map_to": 88, "entity": SENSOR},
    {"topic": "m24", "name": "Custom reading m24", "map_to": 89, "entity": SENSOR},
    {"topic": "m25", "name": "Custom reading m25", "map_to": 90, "entity": SENSOR},
    {"topic": "m26", "name": "Custom reading m26", "map_to": 91, "entity": SENSOR},
    {"topic": "m27", "name": "Custom reading m27", "map_to": 92, "entity": SENSOR},
    {"topic": "m28", "name": "Custom reading m28", "map_to": 93, "entity": SENSOR},
    {"topic": "m29", "name": "Custom reading m29", "map_to": 94, "entity": SENSOR},
    {"topic": "m30", "name": "Custom reading m30", "map_to": 95, "entity": SENSOR},
    # { 'topic': 'uptime', 'name': 'UPTIME', 'map_to': 96, 'entity': SENSOR },
    # { 'topic': 'dewPoint', 'name': 'Dew Point', 'map_to': 100, 'entity': SENSOR },
]
SERIES = {
    LK4_MODEL: LK4_SERIES,
}


# region Functions for building MQTT integration config
def sensors_lookup(name):
    """Return data for entity in SENSORS."""
    return next((item for item in SENSORS if item.name == name), None)


def clean_id(value):
    """HA seems to accept only [A-Za-z0-9_-] in ID, so remove anything else."""
    return re.sub(r"[^A-Za-z0-9_-]+", "", value.replace(" ", "-"))


def get_base_entity(item, device):
    """Generate base for entity."""
    return {
        "unique_id": clean_id(item["name"]),
        "name": item["name"],
        "state_topic": f"{device['prefix']}/{item['topic']}",
    }


def get_device(data, short=False):
    """Return device section for HA entity."""
    device = {
        "identifiers": [clean_id(f"{data['model']}_{data['id']}")],
    }
    if not short:
        device.update(
            {
                "name": data["name"],
                "manufacturer": "tinycontrol",
                "model": data["model"],
                "serial_number": data["mac"],
                "hw_version": data["hw"],
                "sw_version": data["sw"],
            }
        )
    return device


def process_list(list_, device):
    """Add device field into each serie in the list_."""
    tmp = deepcopy(list_)
    for index, item in enumerate(tmp, start=1):
        item["device"] = get_device(device, False if index == 1 else True)
        item["unique_id"] = f"{item['device']['identifiers'][0]}_{item['unique_id']}"
    return tmp


# endregion


# region Generators for SWITCH, BINARY_SENSOR, SENSOR entities
def generate_switches(device, series=None):
    """Generate list of switch sections for HA."""
    switches = []
    items_to_generate = [
        item
        for item in SERIES[device["model"]]
        if item["name"] in series and item["entity"] == SWITCH
    ]
    for item in items_to_generate:
        switch = {
            **get_base_entity(item, device),
            "state_on": "1",
            "state_off": "0",
            "optimistic": True,
            "qos": 0,
            "retain": False,
        }
        if "opt_func" in item:
            switch.update(item["opt_func"](item, device))
        switches.append(switch)
    switches = process_list(switches, device)
    return switches


def generate_binary_sensors(device, series=None):
    """Generate list of binary_sensor sections for HA."""
    binary_sensors = []
    items_to_generate = [
        item
        for item in SERIES[device["model"]]
        if item["name"] in series and item["entity"] == BINARY_SENSOR
    ]
    for item in items_to_generate:
        binary_sensors.append(
            {
                **get_base_entity(item, device),
                "payload_on": "1",
                "payload_off": "0",
                "qos": 0,
            }
        )
    binary_sensors = process_list(binary_sensors, device)
    return binary_sensors


def generate_sensors(device, series=None):
    """Generate list of sensor sections for HA."""
    sensors = []
    items_to_generate = [
        item
        for item in SERIES[device["model"]]
        if item["name"] in series and item["entity"] == SENSOR
    ]
    for item in items_to_generate:
        sensor_reference = sensors_lookup(item["name"])
        sensor = {
            **get_base_entity(item, device),
            "qos": 0,
        }
        if sensor_reference is not None:
            if sensor_reference.device_class is not None:
                sensor["device_class"] = sensor_reference.device_class
            if sensor_reference.suggested_display_precision is not None:
                sensor["suggested_display_precision"] = (
                    sensor_reference.suggested_display_precision
                )
            if sensor_reference.native_unit_of_measurement is not None:
                sensor["native_unit_of_measurement"] = (
                    sensor_reference.native_unit_of_measurement
                )
                sensor["unit_of_measurement"] = (
                    sensor_reference.native_unit_of_measurement
                )
        sensors.append(sensor)
    sensors = process_list(sensors, device)
    return sensors


# endregion


def generate_config(name, model, mac, hw, sw, prefix, series=None):
    """Generate config for device for use with HA mqtt integration.

    model - should match main key in SERIES, and series should match
    name value of any of SERIES[model] items.
    """
    # Grab 6 last characters from MAC for ID (found out a while ago
    # that last 6 may be not unique for LK4)
    device_id = mac.replace(":", "")[:8]
    device = {
        "name": name,
        "model": model,
        "mac": mac,
        "hw": hw,
        "sw": sw,
        "prefix": prefix,
        "id": device_id,
    }
    config = [
        *[{SWITCH: item} for item in generate_switches(device, series)],
        *[{BINARY_SENSOR: item} for item in generate_binary_sensors(device, series)],
        *[{SENSOR: item} for item in generate_sensors(device, series)],
    ]
    return config
