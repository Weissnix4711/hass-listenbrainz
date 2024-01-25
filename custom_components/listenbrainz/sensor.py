"""Sensor platform for listenbrainz."""
from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType

from .api import ListenBrainzUserData
from .const import DOMAIN
from .coordinator import ListenBrainzDataUpdateCoordinator
from .entity import ListenBrainzEntity


@dataclass(frozen=True)
class ListenBrainzSensorEntityDescriptionMixin:
    """Mixin values for listenbrainz sensor entities."""

    value_fn: Callable[[ListenBrainzUserData], StateType]


@dataclass(frozen=True)
class ListenBrainzSensorEntityDescription(
    SensorEntityDescription, ListenBrainzSensorEntityDescriptionMixin
):
    """Class describing listenbrainz sensor entities."""


ENTITY_DESCRIPTIONS = (
    ListenBrainzSensorEntityDescription(
        key="total_listens",
        translation_key="total_listens",
        icon="mdi:music-box-multiple",
        value_fn=lambda data: data.listen_count,
        state_class="total",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        ListenBrainzSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class ListenBrainzSensor(ListenBrainzEntity, SensorEntity):
    """listenbrainz Sensor class."""

    def __init__(
        self,
        coordinator: ListenBrainzDataUpdateCoordinator,
        entity_description: ListenBrainzSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
