"""Custom integration to integrate ListenBrainz with Home Assistant.

For more details about this integration, please refer to
https://github.com/Weissnix4711/hass-listenbrainz
"""
from __future__ import annotations

from datetime import datetime
from time import time

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_TOKEN, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers.typing import ConfigType

from liblistenbrainz import Listen, errors

from .api import ListenBrainzApiClient, ListenBrainzMissingTokenException
from .const import DOMAIN
from .coordinator import ListenBrainzDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.MEDIA_PLAYER]


async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up ListenBrainz integration."""

    async def submit_listen(call: ServiceCall):
        """Submit a single listen."""
        client: ListenBrainzApiClient = hass.data[DOMAIN][
            call.data["config_entry"]
        ].client

        try:
            listened_at = call.data.get("listened_at", None)
            if listened_at is not None:
                listened_at = datetime.strptime(
                    listened_at, "%Y-%m-%d %H:%M:%S"
                ).timestamp()
            else:
                listened_at = time()

            listen = Listen(
                track_name=call.data["track_name"],
                artist_name=call.data["artist_name"],
                listened_at=listened_at,
                release_name=call.data.get("release_name", None),
                additional_info=call.data.get("additional_info", None),
            )

            await client.submit_listen(listen)

        except errors.InvalidSubmitListensPayloadException:
            raise ServiceValidationError(
                translation_domain=DOMAIN, translation_key="invalid_submit_payload"
            )

        except errors.ListenBrainzAPIException as e:
            if e.status_code == 400:
                raise ServiceValidationError(
                    str(e.message),
                    translation_domain=DOMAIN,
                    translation_key="invalid_submit_payload",
                )
            else:
                raise HomeAssistantError(
                    translation_domain=DOMAIN,
                    translation_key="api_exception",
                    translation_placeholders={"code": e.status_code},
                )

        except ListenBrainzMissingTokenException:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="missing_token",
                translation_placeholders={"username": client._username},
            )

    hass.services.async_register(
        domain=DOMAIN, service="submit_listen", service_func=submit_listen
    )

    return True


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator = ListenBrainzDataUpdateCoordinator(
        hass=hass,
        client=ListenBrainzApiClient(
            hass=hass,
            username=entry.data[CONF_USERNAME],
            token=entry.data.get(CONF_API_TOKEN, None),
        ),
        username=entry.data[CONF_USERNAME],
    )
    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
