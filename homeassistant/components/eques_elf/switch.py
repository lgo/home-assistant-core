from __future__ import annotations

import logging

from eques_elf import eques_local
from eques_elf.device import Device
import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

CONF_IP = "ip"
CONF_MAC = "mac"
CONF_PASSWORD = "password"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP): cv.string,
        vol.Required(CONF_MAC): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Eques Elf switch."""
    devices = []
    # Setup manually configured devices.
    # if hass.data[DOMAIN].get(CONF_IP_ADDRESS):
    #     devices.append(
    #         Device(
    #             ip=config[CONF_IP],
    #             mac=config[CONF_MAC],
    #             password=config[CONF_PASSWORD],
    #         )
    #     )

    # Scan for any additional devices.
    devices += eques_local.discover_command()

    add_entities([EquesElfSmartPlug(device) for device in devices])


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Eques Elf smart plug switch device."""
    # TODO(joey): Parse out smart plugs.

    # data = hass.data[DOMAIN][entry.entry_id]
    switches = []
    async_add_entities(switches)


class EquesElfSmartPlug(SwitchEntity):
    """Representation of an Eques Elf smart plug."""

    _attr_icon = "mdi:power-plug"
    _attr_name = "Eques Elf smart plug"

    def __init__(self, device: Device):
        """Initialize the PwrCtrl switch."""
        self._device = device

    @property
    def is_on(self):
        """If the plug is currently on or off."""
        return self._device.state

    def update(self):
        """Trigger update for the plug state."""
        devices = eques_local.status_command(self._device)
        if len(devices) == 1:
            self._device.state = devices[0].devices
        # FIXME(joey): Check for availability.

    def turn_on(self, **kwargs):
        """Turn the plug on."""
        devices = eques_local.on_command(self._device)
        if len(devices) == 1:
            self._device.state = devices[0].devices
        # FIXME(joey): Check for availability.
        self._attr_is_on = True

    def turn_off(self, **kwargs):
        """Turn the plug off."""
        devices = eques_local.off_command(self._device)
        if len(devices) == 1:
            self._device.state = devices[0].devices
        # FIXME(joey): Check for availability.
        self._attr_is_off = True