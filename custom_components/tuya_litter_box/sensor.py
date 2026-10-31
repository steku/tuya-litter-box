"""Sensor platform for Tuya Smart Litter Box."""
from __future__ import annotations

from typing import Any
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfMass, UnitOfTime, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    DP_CAT_WEIGHT,
    DP_TOILET_DURATION,
    DP_VISITS_TODAY,
    DP_LITTER_LEVEL,
    DP_FAULT_CODE,
    DP_CLEAN_SWITCH,
    DP_EMPTY_SWITCH,
)
from .coordinator import TuyaLitterBoxCoordinator

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=DP_CAT_WEIGHT,
        name="Last Cat Weight",
        device_class=SensorDeviceClass.WEIGHT,
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:scale",
    ),
    SensorEntityDescription(
        key=DP_TOILET_DURATION,
        name="Last Visit Duration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key=DP_VISITS_TODAY,
        name="Visits Today",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key=DP_LITTER_LEVEL,
        name="Litter Level",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="cycle_status",
        name="Cycle Status",
        icon="mdi:sync",
    ),
    SensorEntityDescription(
        key=DP_FAULT_CODE,
        name="Fault Code",
        icon="mdi:alert-circle-outline",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    coordinator: TuyaLitterBoxCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        TuyaLitterBoxSensor(coordinator, description)
        for description in SENSORS
    )


class TuyaLitterBoxSensor(
    CoordinatorEntity[TuyaLitterBoxCoordinator], SensorEntity
):
    """Representation of a Tuya Litter Box sensor."""

    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: TuyaLitterBoxCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
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
    def native_value(self):
        """Return the current sensor value."""
        data = self.coordinator.data

        if self.entity_description.key == DP_CAT_WEIGHT:
            raw = data.get(DP_CAT_WEIGHT)
            if raw is not None:
                return round(raw / 1000.0, 2)
            return None

        if self.entity_description.key == "cycle_status":
            if data.get(DP_CLEAN_SWITCH):
                return "cleaning"
            if data.get(DP_EMPTY_SWITCH):
                return "emptying"
            return "idle"

        if self.entity_description.key == DP_VISITS_TODAY:
            return data.get(DP_VISITS_TODAY) or data.get("7", 0)

        return data.get(self.entity_description.key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        attrs: dict[str, Any] = {}
        key = self.entity_description.key
        data = self.coordinator.data

        if key == DP_CAT_WEIGHT:
            attrs["description"] = "Weight of the cat recorded during the most recent visit."
            raw = data.get(DP_CAT_WEIGHT)
            if raw is not None:
                kg = round(raw / 1000.0, 2)
                attrs["weight_kg"] = kg
                attrs["weight_lbs"] = round(kg * 2.20462, 1)
                attrs["weight_raw_grams"] = raw
            if DP_TOILET_DURATION in data:
                attrs["last_duration_seconds"] = data.get(DP_TOILET_DURATION)

        elif key == DP_TOILET_DURATION:
            attrs["description"] = "Duration of the most recent cat visit in seconds."

        elif key == DP_VISITS_TODAY:
            attrs["description"] = "Total number of cat visits recorded today."

        elif key == DP_LITTER_LEVEL:
            attrs["description"] = "Litter bed level percentage."

        elif key == "cycle_status":
            attrs["description"] = "Current operational state of the litter drum (idle, cleaning, or emptying)."

        elif key == DP_FAULT_CODE:
            attrs["description"] = "Hardware diagnostic bitfield (0 = normal, non-zero = fault detected)."
            code = data.get(DP_FAULT_CODE, 0)
            attrs["status"] = "Normal" if code == 0 else f"Fault {code}"

        return attrs
