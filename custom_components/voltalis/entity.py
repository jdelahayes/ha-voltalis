"""Entity representing a Voltalis appliance."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .aiovoltalis.appliance import VoltalisAppliance
from .aiovoltalis.program import VoltalisProgram
from .const import DOMAIN


class VoltalisEntity(CoordinatorEntity):
    """Base class for Voltalis entities."""

    def setupAppliance(
        self,
        coordinator: DataUpdateCoordinator,
        appliance: VoltalisAppliance,
    ) -> None:
        """Initialize the entity.

        Given a appliance id and a short name for the entity, we provide basic device
        info, name, unique id, etc. for all derived entities.
        """
        super().__init__(coordinator)
        self.appliance = appliance
        self._attr_unique_id = str(appliance.id)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(appliance.id))},
            name=appliance.name.capitalize(),
            manufacturer=appliance.modulatorType,
            model=appliance.applianceType,
        )

    def setupProgram(
        self,
        coordinator: DataUpdateCoordinator,
        program: VoltalisProgram,
    ) -> None:
        """Initialize the entity.

        Given a program id and a short name for the entity, we provide basic device
        info, name, unique id, etc. for all derived entities.
        """
    
        super().__init__(coordinator)
        self.program = program
        self._attr_unique_id = str(program.id)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(program.id))},
            name=program.name.capitalize(),
            manufacturer='Voltalis',
            model='Heater Program',
        )
