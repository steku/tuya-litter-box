"""Switch platform for Tuya Smart Litter Box."""
from __future__ import annotations

from typing import Any
from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    DP_AUTO_CLEAN,
    DP_DEODORIZER,
    DP_AUTO_DEODORIZE,
    DP_CHILD_LOCK,
    DP_RADAR_SAFETY,
    DP_SMART_CLEAN,
    DP_CLEAN_DELAY,
    DP_CLEAN_INTERVAL,
    DP_SENSITIVITY,
)
from .coordinator import TuyaLitterBoxCoordinator

SWITCHES: tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key=DP_AUTO_CLEAN,
        name="Auto Clean",
        icon="mdi:broom",
    ),
    SwitchEntityDescription(
        key=DP_DEODORIZER,
        name="Deodorizer",
        icon="mdi:flower",
    ),
    SwitchEntityDescription(
        key=DP_AUTO_DEODORIZE,
        name="Auto Deodorize",
        icon="mdi:fan-auto",
    ),
    SwitchEntityDescription(
        key=DP_CHILD_LOCK,
        name="Child Lock",
        icon="mdi:lock",
    ),
    SwitchEntityDescription(
        key=DP_RADAR_SAFETY,
        name="Safety Radar",
        icon="mdi:radar",
    ),
    SwitchEntityDescription(
        key=DP_SMART_CLEAN,
        name="Smart Clean",
        icon="mdi:shimmer",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switches."""
    coordinator: TuyaLitterBoxCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        TuyaLitterBoxSwitch(coordinator, description)
        for description in SWITCHES
    )


class TuyaLitterBoxSwitch(
    CoordinatorEntity[TuyaLitterBoxCoordinator], SwitchEntity
):
    """Representation of a Tuya Litter Box switch."""

    entity_description: SwitchEntityDescription

    def __init__(
        self,
        coordinator: TuyaLitterBoxCoordinator,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch."""
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
        """Return true if switch is on."""
        return bool(self.coordinator.data.get(self.entity_description.key, False))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        attrs: dict[str, Any] = {}
        key = self.entity_description.key
        data = self.coordinator.data

        descriptions = {
            DP_AUTO_CLEAN: "Automatically sifts waste after a cat finishes and the delay timer elapses.",
            DP_SMART_CLEAN: "Batches clean cycles within the interval window rather than cleaning after every single visit.",
            DP_DEODORIZER: "Toggles the built-in ionic deodorizer module.",
            DP_AUTO_DEODORIZE: "Automatically activates deodorizer after each clean cycle.",
            DP_CHILD_LOCK: "Disables physical buttons on the litter box to prevent accidental activation.",
            DP_RADAR_SAFETY: "Anti-pinch infrared and microwave proximity radar that halts movement if a cat approaches.",
        }

        if key in descriptions:
            attrs["description"] = descriptions[key]

        if key == DP_AUTO_CLEAN:
            if DP_CLEAN_DELAY in data:
                attrs["delay_minutes"] = data.get(DP_CLEAN_DELAY)
            if DP_CLEAN_INTERVAL in data:
                attrs["interval_minutes"] = data.get(DP_CLEAN_INTERVAL)

        if key == DP_RADAR_SAFETY and DP_SENSITIVITY in data:
            attrs["sensitivity_threshold_g"] = data.get(DP_SENSITIVITY)

        return attrs

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.coordinator.async_set_dp(self.entity_description.key, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.coordinator.async_set_dp(self.entity_description.key, False)
