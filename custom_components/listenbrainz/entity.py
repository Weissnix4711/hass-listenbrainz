"""ListenBrainzEntity class."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import ListenBrainzDataUpdateCoordinator


class ListenBrainzEntity(CoordinatorEntity):
    """ListenBrainzEntity class."""

    _attr_attribution = ATTRIBUTION

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ListenBrainzDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.username}_{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.username)},
            name=f"{NAME} {coordinator.username}",
            model=f"{NAME} {coordinator.username}",
            manufacturer=NAME,
            entry_type=DeviceEntryType.SERVICE,
            sw_version=VERSION,
        )
