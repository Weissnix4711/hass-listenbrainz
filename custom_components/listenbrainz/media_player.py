"""Media player platform for listenbrainz."""
from __future__ import annotations
from dataclasses import dataclass

from homeassistant.core import callback
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityDescription,
    MediaPlayerDeviceClass,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)

from .api import ListenBrainzListen
from .const import DOMAIN
from .coordinator import ListenBrainzDataUpdateCoordinator
from .entity import ListenBrainzEntity


@dataclass(frozen=True)
class ListenBrainzMediaPlayerEntityDescriptionMixin:
    """Mixin values for listenbrainz media player entities."""


@dataclass(frozen=True)
class ListenBrainzMediaPlayerEntityDescription(
    MediaPlayerEntityDescription, ListenBrainzMediaPlayerEntityDescriptionMixin
):
    """Class describing listenbrainz media player entities."""


ENTITY_DESCRIPTIONS = (
    ListenBrainzMediaPlayerEntityDescription(
        key="playing_now",
        translation_key="playing_now",
        device_class=MediaPlayerDeviceClass.SPEAKER,
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the media_player platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        ListenBrainzMediaPlayer(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class ListenBrainzMediaPlayer(ListenBrainzEntity, MediaPlayerEntity):
    """Media player for listenbrainz."""

    _attr_supported_features = MediaPlayerEntityFeature(0)
    _attr_media_content_type = MediaType.MUSIC

    def __init__(
        self,
        coordinator: ListenBrainzDataUpdateCoordinator,
        entity_description: ListenBrainzMediaPlayerEntityDescription,
    ) -> None:
        """Initialize the media_player class."""
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description

    @callback
    def _handle_coordinator_update(self) -> None:
        self._set_attr(self.coordinator.data.playing_now)
        self.async_write_ha_state()

    def _set_attr(self, data: ListenBrainzListen | None) -> None:
        self._attr_state = ( MediaPlayerState.PLAYING if data is not None else MediaPlayerState.IDLE )
        self._attr_media_title = ( (data.track_name if not None else None) if data is not None else None )
        self._attr_media_artist = ( (data.artist_name if not None else None) if data is not None else None)
        self._attr_media_track = ( (data.tracknumber if not None else None) if data is not None else None )
        self._attr_media_album_name = ( (data.release_name if not None else None) if data is not None else None )
        self._attr_media_duration = ( (data.duration if not None else None if not None else None) if data is not None else None )
        self._attr_source = ( (data.music_service if not None else None if not None else None) if data is not None else None )
