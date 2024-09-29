"""The Appliance class used by aoivoltalis."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .models import VoltalisApplianceDict, VoltalisApplianceProgrammingDict

if TYPE_CHECKING:
    from . import Voltalis

_LOGGER = logging.getLogger(__name__)


class VoltalisAppliance:
    """Class to represent each Voltalis appliance."""

    _voltalis: Voltalis
    _appliance_json: VoltalisApplianceDict
    _programming: VoltalisApplianceProgramming
    idManualSetting: int
    isReachable: bool

    def __init__(
        self, appliance_json: VoltalisApplianceDict, voltalis: Voltalis
    ) -> None:
        """Set up Voltalis appliance."""
        self._voltalis = voltalis
        self._appliance_json = appliance_json
        self._programming = VoltalisApplianceProgramming(
            programming_json=appliance_json["programming"], voltalisAppliance=self
        )
        self.idManualSetting = 0

    async def async_update(
        self,
    ) -> None:
        """Update appliance throught Voltalis API."""
        await self._voltalis.async_update_appliance(appliance_id=self.id)

    @property
    def id(self) -> int:
        """Get appliance id."""
        return self._appliance_json["id"]

    @property
    def name(self) -> str:
        """Get appliance name."""
        return self._appliance_json["name"]

    @property
    def applianceType(self) -> str:
        """Get appliance type."""
        return self._appliance_json["applianceType"]
    
    @property
    def modulatorType(self) -> str:
        """Get modulator type."""
        return self._appliance_json["modulatorType"]

    @property
    def availableModes(self) -> []:
        """Get available modes."""
        return self._appliance_json["availableModes"]

    @property
    def voltalisVersion(self) -> []:
        """Get voltalis version."""
        return self._appliance_json["voltalisVersion"]

    @property
    def heatingLevel(self) -> []:
        """Get heating level."""
        return self._appliance_json["heatingLevel"]

    @property
    def programming(self) -> []:
        """Get programming."""
        return self._programming

    @property
    def api(self) -> []:
        """Get Voltalis api."""
        return self._voltalis

    def get_json(self) -> []:
        """Get appliance json."""
        return self._appliance_json


class VoltalisApplianceProgramming:
    """Class to represent each Voltalis appliance programming."""

    _appliance: VoltalisAppliance

    def __init__(
        self,
        programming_json: VoltalisApplianceProgrammingDict,
        voltalisAppliance: VoltalisAppliance,
    ) -> None:
        """Set up Voltalis appliance programming."""
        self._programming_json = programming_json
        self._appliance = voltalisAppliance

    @property
    def progType(self) -> str:
        """Get prog type."""
        return self._programming_json["progType"]

    @property
    def progName(self) -> str:
        """Get prog name."""
        return self._programming_json["progName"]

    @property
    def idManualSetting(self) -> int:
        """Get idManualSetting."""
        return self._programming_json["idManualSetting"]

    @property
    def isOn(self) -> bool:
        """Get isOn."""
        return self._programming_json["isOn"]

    @property
    def untilFurtherNotice(self) -> str:
        """Get untilFurtherNotice."""
        return self._programming_json["untilFurtherNotice"]

    @property
    def mode(self) -> str:
        """Get mode."""
        return self._programming_json["mode"]

    @property
    def idPlanning(self) -> int:
        """Get idPlanning."""
        return self._programming_json["idPlanning"]

    @property
    def endDate(self) -> str:
        """Get endDate."""
        return self._programming_json["endDate"]

    @property
    def temperatureTarget(self) -> float:
        """Get temperatureTarget."""
        return self._programming_json["temperatureTarget"]

    @property
    def defaultTemperature(self) -> float:
        """Get defaultTemperature."""
        return self._programming_json["defaultTemperature"]

    def get_json(self) -> []:
        """Get programming json."""
        return self._programming_json
