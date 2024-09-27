"""Platform for switch integration."""
from __future__ import annotations

import logging

from homeassistant.components.switch import (SwitchEntity)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    VOLTALIS_CONTROLLER,
)
from .entity import VoltalisEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    controller = hass.data[DOMAIN][entry.entry_id][VOLTALIS_CONTROLLER]
    entities = []
    for program in controller.programs:
        entities.append(VoltalisProgram(controller.coordinator, program))
    async_add_entities(entities)

class VoltalisProgram(VoltalisEntity, SwitchEntity):
    """Voltalis program."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_icon = "mdi:toggle-switch"

    def __init__(self, coordinator, program):
        """Initialize the entity."""
        super().setupProgram(coordinator, program)

    @property
    def is_on(self) -> bool:
        return self.program.isEnabled

    async def async_turn_on(self, **kwargs) -> None:
        await self.async_set_state(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self.async_set_state(False)


    async def async_set_state(self, state:bool) -> None:
        curjson = {
            "name": self.program.name,
            "enabled": state,
        }
        await self.program.api.async_set_program_state(
            json = curjson,
            program_id = self.program.id
        )
