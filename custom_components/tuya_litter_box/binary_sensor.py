"""Binary sensor platform for Tuya Smart Litter Box."""
from __future__ import annotations

from typing import Any
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DP_BIN_FULL, DP_CAT_OCCUPANCY
from .coordinator import TuyaLitterBoxCoordinator

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key=DP_BIN_FULL,
        name="Waste Drawer Full",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:trash-can-alert",
    ),
    BinarySensorEntityDescription(
        key=DP_CAT_OCCUPANCY,
        name="Cat Occupancy",
        device_class=BinarySensorDeviceClass.OCCUPANCY,
        icon="mdi:cat",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""
    coordinator: TuyaLitterBoxCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        TuyaLitterBoxBinarySensor(coordinator, description)
        for description in BINARY_SENSORS
    )


class TuyaLitterBoxBinarySensor(
    CoordinatorEntity[TuyaLitterBoxCoordinator], BinarySensorEntity
):
    """Representation of a Tuya Litter Box binary sensor."""

    entity_description: BinarySensorEntityDescription

    def __init__(
        self,
        coordinator: TuyaLitterBoxCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.device_id}_{description.key}"
        self._attr_name = description.name

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.device_id)},
            "name": "Smart Litter Box",
            "manufacturer": "Tuya / Tonepie",
            "model": "T1 Pro Compatible",
        }

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return bool(self.coordinator.data.get(self.entity_description.key, False))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        attrs: dict[str, Any] = {}
        key = self.entity_description.key

        descriptions = {
            DP_BIN_FULL: "Optical sensor beam across the waste drawer. Triggers when the waste pile reaches capacity.",
            DP_CAT_OCCUPANCY: "Weight and presence detection indicating if a cat is currently inside the litter box.",
        }

        if key in descriptions:
            attrs["description"] = descriptions[key]

        return attrs
