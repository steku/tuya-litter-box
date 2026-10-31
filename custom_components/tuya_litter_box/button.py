"""Button platform for Tuya Smart Litter Box."""
from __future__ import annotations

from typing import Any
from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DP_CLEAN_SWITCH, DP_EMPTY_SWITCH
from .coordinator import TuyaLitterBoxCoordinator

BUTTONS: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(
        key=DP_CLEAN_SWITCH,
        name="Clean Now",
        icon="mdi:broom",
    ),
    ButtonEntityDescription(
        key=DP_EMPTY_SWITCH,
        name="Empty Drum",
        icon="mdi:trash-can-outline",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up buttons."""
    coordinator: TuyaLitterBoxCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        TuyaLitterBoxButton(coordinator, description)
        for description in BUTTONS
    )


class TuyaLitterBoxButton(
    CoordinatorEntity[TuyaLitterBoxCoordinator], ButtonEntity
):
    """Representation of a Tuya Litter Box action button."""

    entity_description: ButtonEntityDescription

    def __init__(
        self,
        coordinator: TuyaLitterBoxCoordinator,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
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
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        attrs: dict[str, Any] = {}
        key = self.entity_description.key

        descriptions = {
            DP_CLEAN_SWITCH: "Triggers an immediate rotation cycle to sift waste into the collection drawer.",
            DP_EMPTY_SWITCH: "Triggers a reverse rotation cycle to dump all clean litter into the waste drawer for replacement.",
        }

        if key in descriptions:
            attrs["description"] = descriptions[key]

        return attrs

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_set_dp(self.entity_description.key, True)
