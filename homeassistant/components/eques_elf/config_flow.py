"""Config flow for Eques Elf."""
import logging

from eques_elf import eques_local

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


# from homeassistant import config_entries
# from .const import DOMAIN


# class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
#     """Example config flow."""


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    _LOGGER.warning("running eques_elf discover")
    devices = await hass.async_add_executor_job(eques_local.discover_command)
    return len(devices) > 0


config_entry_flow.register_discovery_flow(DOMAIN, "Eques Elf", _async_has_devices)
