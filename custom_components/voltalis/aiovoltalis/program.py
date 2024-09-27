"""The Appliance class used by aoivoltalis."""
from __future__ import annotations
from enum import Enum

import logging
from typing import TYPE_CHECKING

from .models import VoltalisProgramDict

if TYPE_CHECKING:
    from . import Voltalis

_LOGGER = logging.getLogger(__name__)

class ProgramType(Enum):
    """Enum to differentiate Default and User heater programs."""
    DEFAULT = "DEFAULT"
    USER = "USER"

class VoltalisProgram:
    """Class to represent each Voltalis program."""

    _voltalis: Voltalis
    _program_json: VoltalisProgramDict
    _program_type: ProgramType

    def __init__(
        self, appliance_json: VoltalisProgramDict, voltalis: Voltalis, _program_type: ProgramType
    ) -> None:
        """Set up Voltalis appliance."""
        self._voltalis = voltalis
        self._program_json = appliance_json
        self._program_type = _program_type

    async def async_update(
        self,
    ) -> None:
        """Update only user programs."""
        if self._program_type == ProgramType.USER:
            await self._voltalis.async_update_user_program(program_id=self.id)

    @property
    def id(self) -> int:
        """Get appliance id."""
        return self._program_json["id"]

    @property
    def name(self) -> str:
        """Get appliance name."""
        return self._program_json["name"]

    @property
    def isEnabled(self) -> bool:
        """Get appliance isEnabled."""
        return self._program_json["enabled"]

    @property
    def api(self) -> []:
        """Get Voltalis api."""
        return self._voltalis

    def get_json(self) -> []:
        """Get program json"""
        return self._program_json

