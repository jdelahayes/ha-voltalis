"""An asynchronous client for Voltalis API."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

from aiohttp.client import ClientSession, ClientTimeout
from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientError,
    ClientResponseError,
)

from . import const as CONST
from .exceptions import VoltalisAuthenticationException, VoltalisException
from .appliance import VoltalisAppliance

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Voltalis:
    """Main Voltalis class."""

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        auto_login: bool = False,
        session: ClientSession | None = None,
    ) -> None:
        self._username = username
        self._password = password
        self._auto_login = auto_login
        self._appliances: dict[int, VoltalisAppliance] = {}

        if session is None:
            session = ClientSession()
            self._close_session = True
        self._session = session

        # Create a new cache template
        self._cache: dict[str, str] = {
            CONST.AUTH_TOKEN: "",
            CONST.DEFAULT_SITE_ID: "",
        }

    async def __aenter__(self) -> Voltalis:
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        """Async exit."""
        await self.async_logout()
        if self._session and self._close_session:
            await self._session.close()

    async def async_initialize(self) -> list[VoltalisAppliance]:
        if (
            self._username is not None
            and self._password is not None
            and self._auto_login
        ):
            await self.async_login()

        await self.async_get_default_site_id()
        await self.async_get_appliances()
        return list(self._appliances.values())

    def cache(self, key: str) -> str:
        """Get a cached value."""
        return self._cache.get(key, "")

    def update_cache(self, key: str, value: str) -> None:
        """Update a cached value."""
        self._cache.update({key: value})

    async def async_login(self) -> bool:
        """Execute Voltalis login."""
        _LOGGER.debug("Login start")
        login_data: dict[str, str | int] = {
            "login": self._username,
            "password": self._password,
        }
        response = await self.async_send_request(
            CONST.LOGIN_URL, json=login_data, retry=False, method=CONST.HTTPMethod.POST
        )
        _LOGGER.debug("Login Response: %s", response)
        self.update_cache(CONST.AUTH_TOKEN, response["token"])
        _LOGGER.info("Login successful")

    async def async_logout(self) -> bool:
        """Execute Voltalis logout."""
        response = await self.async_send_request(
            CONST.LOGOUT_URL, retry=False, method=CONST.HTTPMethod.DELETE
        )
        _LOGGER.info("Logout successful")

    async def async_get_default_site_id(self) -> int:
        """Get Voltalis account default site id"""
        _LOGGER.debug("Get default site id start")
        response = await self.async_send_request(
            CONST.ACCOUNT_ME_URL, retry=False, method=CONST.HTTPMethod.GET
        )
        self.update_cache(CONST.DEFAULT_SITE_ID, response["defaultSite"]["id"])
        _LOGGER.info("Default site id = %s", self.cache(CONST.DEFAULT_SITE_ID))
        return self.cache(CONST.DEFAULT_SITE_ID)

    async def async_get_appliances(self) -> list[VoltalisAppliance]:
        """Get all Voltalis appliances"""
        _LOGGER.debug("Get all Voltalis appliances")
        appliances_json = await self.async_send_request(
            CONST.APPLIANCE_URL, retry=False, method=CONST.HTTPMethod.GET
        )
        for appliance_json in appliances_json:
            appliance = VoltalisAppliance(appliance_json, self)
            self._appliances[appliance.id] = appliance

        await self.async_update_manualsettings()

        return list(self._appliances.values())

    async def async_update_manualsettings(self) -> None:
        """Get all Voltalis appliances manual settings"""
        _LOGGER.debug("Get all Voltalis appliances manual settings")
        manualsettings_json = await self.async_send_request(
            CONST.MANUAL_SETTING_URL, retry=False, method=CONST.HTTPMethod.GET
        )
        for manualsetting_json in manualsettings_json:
            _LOGGER.debug(
                f"Update appliance {manualsetting_json['idAppliance']} manual setting id to {manualsetting_json['id']}"
            )
            self._appliances[
                manualsetting_json["idAppliance"]
            ].idManualSetting = manualsetting_json["id"]

    async def async_update_appliance(self, appliance_id: int) -> None:
        """Get a Voltalis appliance"""
        _LOGGER.debug(f"Update Voltalis appliance {appliance_id}")
        appliance_json = await self.async_send_request(
            f"{CONST.APPLIANCE_URL}/{appliance_id}",
            retry=False,
            method=CONST.HTTPMethod.GET,
        )
        self._appliances[appliance_id]._appliance_json = appliance_json
        self._appliances[appliance_id]._programming._programming_json = appliance_json[
            "programming"
        ]

    async def async_set_manualsetting(
        self,
        programming_id: int,
        **kwargs: Any,
    ) -> None:
        """Set Voltalis appliance manual settings"""
        _LOGGER.debug(f"Set Voltalis appliance programming {programming_id} ")
        _LOGGER.debug(f"json = {kwargs.get('json','empty')}")

        appliance_json = await self.async_send_request(
            f"{CONST.MANUAL_SETTING_URL}/{programming_id}",
            retry=False,
            method=CONST.HTTPMethod.PUT,
            **kwargs,
        )

    async def async_send_request(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        method: CONST.HTTPMethod = CONST.HTTPMethod.GET,
        retry: bool = True,
        **kwargs: Any,
    ) -> Any:
        """Send http requests to Voltalis."""

        if len(self.cache(CONST.AUTH_TOKEN)) == 0 and url != CONST.LOGIN_URL:
            await self.async_login()

        headers = headers if headers else {}
        if len(self.cache(CONST.AUTH_TOKEN)) > 0:
            headers["Authorization"] = f"Bearer {self.cache(CONST.AUTH_TOKEN)}"
        headers["content-type"] = "application/json"
        headers["accept"] = "*/*"

        # Replace url placeholder
        if url.rfind("__site__") > 0:
            url = url.replace("__site__", str(self.cache(CONST.DEFAULT_SITE_ID)))

        _LOGGER.debug("Call Voltalise API")

        try:
            response = await self._session.request(
                method.value,
                url,
                headers=headers,
                timeout=ClientTimeout(30),
                **kwargs,
            )
            if response.status == 401:
                raise VoltalisAuthenticationException(await response.text())
            if response.status == 404:
                _LOGGER.exception(await response.text())
                return None
            response.raise_for_status()
        except (ClientConnectorError, ClientError, ClientResponseError) as ex:
            if retry:
                await self.async_login()
                return await self.async_send_request(
                    url, headers=headers, method=method, retry=False, **kwargs
                )
            raise VoltalisException from ex

        _LOGGER.debug("End call to Voltalise API")

        if response.content_type == "application/json":
            return await response.json()

        return await response.read()
