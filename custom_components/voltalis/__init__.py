"""Voltalis integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, VOLTALIS_CONTROLLER
from .controller import VoltalisController

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.WATER_HEATER, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up voltalis from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    controller = VoltalisController(hass)
    hass.data[DOMAIN][entry.entry_id] = {
        VOLTALIS_CONTROLLER: controller,
    }

    if not await controller.async_setup_entry(entry):
        return False

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
