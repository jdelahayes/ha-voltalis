"""Constants for the voltalis integration."""

from homeassistant.components.climate import (
    PRESET_AWAY,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_HOME,
)

DEFAULT_NAME = "Voltalis"
DOMAIN = "voltalis"

VOLTALIS_CONTROLLER = "voltalis_controller"

VOLTALIS_PRESET_MODES = {
    PRESET_ECO: "ECO",
    PRESET_COMFORT: "CONFORT",
    PRESET_HOME: "TEMPERATURE",
    PRESET_AWAY: "HORS_GEL",
}

HA_PRESET_MODES = {
    "ECO": PRESET_ECO,
    "CONFORT": PRESET_COMFORT,
    "TEMPERATURE": PRESET_HOME,
    "HORS_GEL": PRESET_AWAY,
}

SCAN_INTERVAL = 60
POLLING_TIMEOUT = 10

DEFAULT_MIN_TEMP = 7
DEFAULT_MAX_TEMP = 24

ATTR_STATUS = "status"
