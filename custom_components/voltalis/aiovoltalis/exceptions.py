"""The exceptions used by aiovoltalis."""
from __future__ import annotations


class VoltalisException(Exception):
    """Class to throw general skybell exception."""


class VoltalisAuthenticationException(VoltalisException):
    """Class to throw authentication exception."""
