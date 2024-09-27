"""Interface to the Voltalis API."""

import asyncio
from datetime import timedelta
import logging

from aiohttp import client_exceptions

from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .aiovoltalis import (
    Voltalis,
    VoltalisAuthenticationException,
    VoltalisException,
)
from .const import DOMAIN, POLLING_TIMEOUT, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class VoltalisController:
    """Interface between Home Assistant and the Votalis API."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize an interface to Voltalis."""
        self._hass = hass
        self._voltalis = None
        self.appliances = None
        self.programs = None
        self.coordinator = None

    async def async_setup_entry(self, entry):
        """Perform initial setup.

        Authenticate, query static state, set up polling, and otherwise make
        ready for normal operations .
        """

        try:
            self._voltalis = Voltalis(
                username=entry.data[CONF_EMAIL],
                password=entry.data[CONF_PASSWORD],
                auto_login=True,
                session=async_get_clientsession(self._hass),
            )
        except VoltalisAuthenticationException as ex:
            # credentials were changed or invalidated, we need new ones
            raise ConfigEntryAuthFailed from ex
        except (
            asyncio.TimeoutError,
            client_exceptions.ClientOSError,
            client_exceptions.ServerDisconnectedError,
            client_exceptions.ContentTypeError,
        ) as err:
            raise ConfigEntryNotReady from err

        await self._voltalis.async_initialize()
        self.appliances = await self._voltalis.async_get_appliances()
        self.programs = await self._voltalis.async_get_programs()

        self.coordinator = DataUpdateCoordinator(
            self._hass,
            _LOGGER,
            name=DOMAIN,
            update_method=self.async_update_data,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

        await self.coordinator.async_refresh()

        self.async_register_devices(entry)

        return True

    async def async_update_data(self):
        """Query the API and return the new state."""
        try:
            async with asyncio.timeout(POLLING_TIMEOUT):
                for appliance in self.appliances:
                    await appliance.async_update()
                await self._voltalis.async_update_appliances_diagnostics()

            async with asyncio.timeout(POLLING_TIMEOUT):
                for program in self.programs:
                    await program.async_update()
                    
        except VoltalisException as err:
            raise UpdateFailed(err) from err

    @callback
    def async_register_devices(self, entry):
        device_registry = dr.async_get(self._hass)

        """Register devices with the device registry for all Appliances."""
        for appliance in self.appliances:
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, str(appliance.id))},
                name=appliance.name.capitalize(),
                manufacturer=appliance.modulatorType,
                model=appliance.applianceType,
            )

        """Register devices with the device registry for all Programs."""
        for program in self.programs:
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, str(program.id))},
                name=program.name.capitalize(),
                entry_type=dr.DeviceEntryType.SERVICE 
            )


