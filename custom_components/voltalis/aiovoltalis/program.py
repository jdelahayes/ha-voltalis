"""The Appliance class used by aoivoltalis."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from .models import VoltalisProgramDict

if TYPE_CHECKING:
    from . import Voltalis

_LOGGER = logging.getLogger(__name__)


class VoltalisProgram:
    """Class to represent each Voltalis program."""

    _voltalis: Voltalis
    _program_json: VoltalisProgramDict

    def __init__(
        self, appliance_json: VoltalisProgramDict, voltalis: Voltalis
    ) -> None:
        """Set up Voltalis appliance."""
        self._voltalis = voltalis
        self._program_json = appliance_json

    async def async_update(
        self,
    ) -> None:
        await self._voltalis.async_update_program(program_id=self.id)

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

