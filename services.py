"""Services/actions for tinycontrol integration.

It contains:
- add_mqtt_device - experimental action for adding devices that uses MQTT for communication,
so it depends on built-in MQTT integration.
"""

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components import mqtt
from homeassistant.components.mqtt.const import (
    DOMAIN as MQTT_DOMAIN,
    CONF_DISCOVERY_PREFIX,
)
import json
from homeassistant.core import HomeAssistant, ServiceCall
from typing import Iterable
from .mqtt_integration import LK4_MODEL, LK4_SERIES, generate_config, clean_id

from .const import DOMAIN


# For now only one device_model - LK4, others might be added as separate actions,
# so the schema is clean, also note that services.yaml keeps options of series.
ADD_MQTT_DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required("device_name"): cv.string,
        vol.Required("device_model"): vol.In([LK4_MODEL]),
        vol.Required("serial_number"): cv.string,
        vol.Required("hw_version"): cv.string,
        vol.Required("sw_version"): cv.string,
        vol.Required("topic_prefix"): cv.string,
        vol.Required("series"): vol.All(
            [vol.In([item["name"] for item in LK4_SERIES])], vol.Length(min=1)
        ),
        vol.Optional(
            "discovery_prefix"
        ): cv.string,  # fallback to MQTT option or "homeassistant"
    }
)


async def async_setup_services(hass: HomeAssistant):
    """Setup tinycontrol services."""
    if not hass.services.has_service(DOMAIN, "add_mqtt_device"):

        def _get_mqtt_discovery_prefix() -> str:
            """Helper for getting MQTT discovery prefix."""
            # Try to read the currently configured prefix from the MQTT integration config entry.
            dp = "homeassistant"
            try:
                mqtt_entries = hass.config_entries.async_entries(MQTT_DOMAIN)
                if mqtt_entries:
                    me = mqtt_entries[0]
                    dp = me.options.get(
                        CONF_DISCOVERY_PREFIX, me.data.get(CONF_DISCOVERY_PREFIX, dp)
                    )
            except Exception:  # be robust
                pass
            return dp

        async def handle_add_mqtt_device(call: ServiceCall) -> None:
            """Service handler for adding device in MQTT integration."""
            if not hass.config_entries.async_entries(MQTT_DOMAIN):
                # Give a clear error if MQTT isn't set up
                raise HomeAssistantError("MQTT is not set up in Home Assistant")
            data = dict(call.data)
            device_name = data["device_name"]
            device_model = data["device_model"]
            serial = data["serial_number"]
            hw = data["hw_version"]
            sw = data["sw_version"]
            topic_prefix = data["topic_prefix"].rstrip("/")
            series: Iterable[str] = data["series"]
            discovery_prefix = (
                data.get("discovery_prefix") or _get_mqtt_discovery_prefix()
            )

            # Build set of messages and send them
            mqtt_config = generate_config(
                device_name, device_model, serial, hw, sw, topic_prefix, series
            )
            for config_item in mqtt_config:
                for component, entity_val in config_item.items():
                    # Actually there is only one iteration in this loop, because each config_item
                    # is a dict describing single entry.
                    # Ensure that object_id has valid format.
                    object_id = clean_id(entity_val["name"])
                    await mqtt.async_publish(
                        hass,
                        f"{discovery_prefix}/{component}/{object_id}/{entity_val['unique_id']}/config",
                        json.dumps(entity_val, ensure_ascii=False),
                        qos=1,
                        retain=True,
                    )

        hass.services.async_register(
            DOMAIN,
            "add_mqtt_device",
            handle_add_mqtt_device,
            schema=ADD_MQTT_DEVICE_SCHEMA,
        )
        # Mark that services are registered (optional bookkeeping)
        hass.data.setdefault(DOMAIN, {})["services_registered"] = True


async def async_unload_services(hass: HomeAssistant, unload_status: bool):
    """Unload tinycontrol services."""
    # If no more entries left, remove the service
    if unload_status and not hass.config_entries.async_entries(DOMAIN):
        if hass.services.has_service(DOMAIN, "add_mqtt_device"):
            hass.services.async_remove(DOMAIN, "add_mqtt_device")
