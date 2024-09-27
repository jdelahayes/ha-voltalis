"""Platform for climate integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.water_heater import WaterHeaterEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    VOLTALIS_CONTROLLER,
    VOLTALIS_WATERHEATER_TYPE,
)
from .entity import VoltalisEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up water heater entity for Voltalis Appliance."""
    controller = hass.data[DOMAIN][entry.entry_id][VOLTALIS_CONTROLLER]
    entities = []
    for appliance in controller.appliances:
        if appliance.applianceType == VOLTALIS_WATERHEATER_TYPE:
            entities.append(VoltalisWaterHeater(controller.coordinator, appliance))
    async_add_entities(entities)


class VoltalisWaterHeater(VoltalisEntity, WaterHeaterEntity):
    """Voltalis Water Heater."""

    _attr_has_entity_name = True
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, appliance):
        """Initialize the entity."""
        super().setupAppliance(coordinator, appliance)

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        return self.appliance.programming.temperatureTarget

    def set_operation_mode(self, operation_mode: str) -> None:
        """Set new target operation mode."""
        raise NotImplementedError()

    def set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        raise NotImplementedError()

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the water heater on."""
        raise NotImplementedError()

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the water heater off."""
        raise NotImplementedError()

    def turn_away_mode_on(self) -> None:
        """Turn away mode on."""
        raise NotImplementedError()

    def turn_away_mode_off(self) -> None:
        """Turn away mode off."""
        raise NotImplementedError()
