"""Platform for climate integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.unit_conversion import TemperatureConverter

from .const import (
    DEFAULT_MAX_TEMP,
    DEFAULT_MIN_TEMP,
    DOMAIN,
    HA_PRESET_MODES,
    VOLTALIS_CONTROLLER,
    VOLTALIS_PRESET_MODES,
    VOLTALIS_HEATER_TYPE,
)
from .entity import VoltalisEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up climate entity for Voltalis Appliance."""
    controller = hass.data[DOMAIN][entry.entry_id][VOLTALIS_CONTROLLER]
    entities = []
    for appliance in controller.appliances:
        if appliance.applianceType == VOLTALIS_HEATER_TYPE:
            entities.append(VoltalisClimate(controller.coordinator, appliance))
    async_add_entities(entities)


class VoltalisClimate(VoltalisEntity, ClimateEntity):
    """Voltalis climate."""

    _attr_has_entity_name = True
    _attr_hvac_mode = HVACMode.HEAT
    _attr_hvac_modes = [HVACMode.AUTO, HVACMode.HEAT, HVACMode.OFF]
    _attr_preset_modes = list(HA_PRESET_MODES.values())
    _attr_max_temp = DEFAULT_MAX_TEMP
    _attr_min_temp = DEFAULT_MIN_TEMP
    _attr_supported_features = (
        ClimateEntityFeature.PRESET_MODE | ClimateEntityFeature.TARGET_TEMPERATURE
    )
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, appliance):
        """Initialize the entity."""
        super().__init__(coordinator, appliance, "Appliance")

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current running hvac operation."""
        if self.appliance.programming.isOn:
            return HVACAction.HEATING
        return HVACAction.OFF

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return hvac operation ie. heat, cool mode."""
        if self.appliance.programming.progType == "MANUAL":
            if not self.appliance.programming.isOn:
                return HVACMode.OFF
            return HVACMode.HEAT
        if self.appliance.programming.progType == "USER":
            return HVACMode.AUTO
        return self._attr_hvac_mode

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        _LOGGER.debug(
            "Set Voltalis appliance %s HVAC Mode to %s", self.appliance.id, hvac_mode
        )

        curjson = {
            "id": self.appliance.idManualSetting,
            "enabled": True,
            "idAppliance": self.appliance.id,
            "applianceName": self.appliance.name,
            "applianceType": self.appliance.applianceType,
            "untilFurtherNotice": self.appliance.programming.untilFurtherNotice,
            "mode": self.appliance.programming.mode,
            "heatingLevel": self.appliance.heatingLevel,
            "endDate": self.appliance.programming.endDate,
            "temperatureTarget": self.appliance.programming.temperatureTarget,
            "isOn": self.appliance.programming.isOn,
        }

        if hvac_mode == HVACMode.HEAT:
            # HVACMode.HEAT -> Manual setting enable: off, untilFurtherNotice: true
            curjson["enabled"] = True
            curjson["mode"] = "TEMPERATURE"
            curjson["untilFurtherNotice"] = True
            await self.appliance.api.async_set_manualsetting(
                json=curjson, programming_id=self.appliance.idManualSetting
            )
            await self.coordinator.async_request_refresh()
        elif hvac_mode == HVACMode.OFF:
            # HVACMode.OFF -> Manual setting enable: off, isOn: false
            curjson["enabled"] = True
            curjson["isOn"] = False
            curjson["untilFurtherNotice"] = True
            await self.appliance.api.async_set_manualsetting(
                json=curjson, programming_id=self.appliance.idManualSetting
            )
            await self.coordinator.async_request_refresh()
        elif hvac_mode == HVACMode.AUTO:
            # HVACMode.AUTO -> Manual setting enable: False
            curjson["enabled"] = False
            await self.appliance.api.async_set_manualsetting(
                json=curjson, programming_id=self.appliance.idManualSetting
            )
            await self.coordinator.async_request_refresh()

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        min_temp = DEFAULT_MIN_TEMP
        return TemperatureConverter.convert(
            min_temp, UnitOfTemperature.CELSIUS, self.temperature_unit
        )

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        max_temp = DEFAULT_MAX_TEMP
        return TemperatureConverter.convert(
            max_temp, UnitOfTemperature.CELSIUS, self.temperature_unit
        )

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode."""
        return HA_PRESET_MODES[self.appliance.programming.mode]

    @property
    def target_temperature(self) -> float:
        """Return the target temperature."""
        return self.appliance.programming.temperatureTarget

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs[ATTR_TEMPERATURE]
        request_body = {
            "id": self.appliance.idManualSetting,
            "enabled": True,
            "idAppliance": self.appliance.id,
            "applianceName": self.appliance.name,
            "applianceType": self.appliance.applianceType,
            "untilFurtherNotice": True,
            "mode": "TEMPERATURE",
            "heatingLevel": self.appliance.heatingLevel,
            "endDate": None,
            "temperatureTarget": temperature,
            "isOn": True,
        }
        await self.appliance.api.async_set_manualsetting(
            json=request_body, programming_id=self.appliance.idManualSetting
        )
        await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Activate the specified preset mode."""

        request_body = {
            "id": self.appliance.idManualSetting,
            "enabled": True,
            "idAppliance": self.appliance.id,
            "applianceName": self.appliance.name,
            "applianceType": self.appliance.applianceType,
            "untilFurtherNotice": True,
            "mode": VOLTALIS_PRESET_MODES[preset_mode],
            "heatingLevel": self.appliance.heatingLevel,
            "endDate": None,
            "temperatureTarget": self.appliance.programming.temperatureTarget,
            "isOn": True,
        }
        await self.appliance.api.async_set_manualsetting(
            json=request_body, programming_id=self.appliance.idManualSetting
        )
        await self.coordinator.async_request_refresh()
