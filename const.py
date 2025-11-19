"""Constants for the tinycontrol integration."""

import logging
from datetime import timedelta

# Integration domain
DOMAIN = "tinycontrol"

LOGGER = logging.getLogger(__package__)
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)
