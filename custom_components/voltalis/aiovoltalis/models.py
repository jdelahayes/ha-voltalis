"""Models for Voltalis."""
from __future__ import annotations


class VoltalisApplianceDict(dict):
    """Class for Voltalis appliance Dict."""

    id: int
    name: str
    applianceType: str
    modulatorType: str
    availableModes: []
    voltalisVersion: str
    programming: VoltalisApplianceProgrammingDict
    heatingLevel: int


class VoltalisApplianceProgrammingDict(dict):
    """Class for Voltalis appliance programming Dict."""

    progType: str
    progName: str
    idManualSetting: int
    isOn: bool
    untilFurtherNotice: bool
    mode: str
    idPlanning: int
    endDate: str
    temperatureTarget: float
    defaultTemperature: float
