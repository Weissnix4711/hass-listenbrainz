"""DataUpdateCoordinator for listenbrainz."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from liblistenbrainz.errors import ListenBrainzAPIException

from .api import (
    ListenBrainzApiClient,
)
from .const import LOGGER, NAME


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class ListenBrainzDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: ListenBrainzApiClient,
        username: str,
    ) -> None:
        """Initialize."""
        self.client = client
        self.username = username
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=f"{NAME} {username}",
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.client.async_update_data()
        except ListenBrainzAPIException as exception:
            raise UpdateFailed(exception)
