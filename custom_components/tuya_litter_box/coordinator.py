"""DataUpdateCoordinator for Tuya Smart Litter Box."""
from __future__ import annotations

import logging
from datetime import timedelta
import tinytuya

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    CONF_DEVICE_ID,
    CONF_IP_ADDRESS,
    CONF_LOCAL_KEY,
    CONF_PROTOCOL_VERSION,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class TuyaLitterBoxCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to fetch status from the Tuya Litter Box."""

    def __init__(self, hass: HomeAssistant, entry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.device_id: str = entry.data[CONF_DEVICE_ID]
        self.ip_address: str = entry.data[CONF_IP_ADDRESS]
        self.local_key: str = entry.data[CONF_LOCAL_KEY]
        
        version_str = str(entry.data.get(CONF_PROTOCOL_VERSION, "3.5"))
        try:
            self.version = float(version_str)
        except ValueError:
            self.version = 3.5

        scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.device_id}",
            update_interval=timedelta(seconds=scan_interval),
        )

        self._device = tinytuya.Device(self.device_id, self.ip_address, self.local_key)
        self._device.set_version(self.version)
        self._device.set_socketTimeout(5)

    def _sync_fetch_status(self) -> dict:
        """Synchronously fetch status from device."""
        status = self._device.status()
        if "Error" in status:
            raise UpdateFailed(f"Tuya device error: {status['Error']}")
        return status.get("dps", {})

    async def _async_update_data(self) -> dict:
        """Fetch data from device in an executor job."""
        return await self.hass.async_add_executor_job(self._sync_fetch_status)

    def _sync_set_dp(self, dp_id: str, value) -> bool:
        """Synchronously set a data point value."""
        return self._device.set_status(value, dp_id)

    async def async_set_dp(self, dp_id: str, value) -> bool:
        """Set a data point value asynchronously."""
        res = await self.hass.async_add_executor_job(self._sync_set_dp, dp_id, value)
        await self.async_request_refresh()
        return res

