"""listenbrainz API Client."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass


from homeassistant.core import HomeAssistant

from liblistenbrainz import ListenBrainz, Listen
from liblistenbrainz.errors import (
    ListenBrainzAPIException,
    ListenBrainzException,
    InvalidAuthTokenException,
    InvalidSubmitListensPayloadException,
    AuthTokenRequiredException,
)


class ListenBrainzUnknownUserException(ListenBrainzException):
    """User does not exist."""


class ListenBrainzInvalidTokenException(InvalidAuthTokenException):
    """Token invalid."""


class ListenBrainzMissingTokenException(AuthTokenRequiredException):
    """Token not set up."""


class ListenBrainzInvalidSubmitPayloadException(InvalidSubmitListensPayloadException):
    """Invalid payload for listen submit."""


@dataclass(frozen=True)
class ListenBrainzListenMixin:
    """Mixin values for listenbrainz listens."""

    duration: int | None
    music_service: str | None


@dataclass(frozen=True)
class ListenBrainzListen(Listen, ListenBrainzListenMixin):
    """Class describing listenbrainz listens."""


@dataclass
class ListenBrainzUserData:
    """Representation of user data."""

    listen_count: int
    playing_now: ListenBrainzListen


class ListenBrainzApiClient:
    """listenbrainz API Client."""

    def __init__(
        self,
        hass: HomeAssistant,
        username: str,
        token: str | None,
    ) -> None:
        """Listenbrainz API Client."""
        self._hass = hass
        self._username = username
        self._token = token
        self.client = ListenBrainz()

        if self._token is not None:
            try:
                asyncio.run_coroutine_threadsafe(self.async_set_token(), hass.loop)
            except InvalidAuthTokenException:
                raise ListenBrainzInvalidTokenException
            except ListenBrainzAPIException as e:
                raise e

    async def async_set_token(self) -> None:
        """Set the token to be used by the client."""
        await self._hass.async_add_executor_job(self._set_token)

    async def validate_input(self) -> None:
        """Validate username/token if used."""
        await self._hass.async_add_executor_job(self._get_listen_count)
        if self._token is not None:
            valid = await self._hass.async_add_executor_job(self._is_token_valid)
            if not valid:
                raise ListenBrainzInvalidTokenException

    async def async_update_data(self) -> ListenBrainzUserData:
        """Get data."""
        try:
            listen_count = await self._hass.async_add_executor_job(
                self._get_listen_count
            )
            playing_now = await self._hass.async_add_executor_job(self._get_playing_now)
        except ListenBrainzAPIException as e:
            raise e
        return ListenBrainzUserData(listen_count=listen_count, playing_now=playing_now)

    async def submit_listen(self, listen: Listen) -> any:
        """Submit a listen."""
        if self._token is not None:
            try:
                response = await self._hass.async_add_executor_job(
                    self._submit_listen, listen
                )
            except InvalidSubmitListensPayloadException as e:
                raise e
            except ListenBrainzAPIException as e:
                raise e
            except AuthTokenRequiredException:
                raise ListenBrainzMissingTokenException
            else:
                return response
        else:
            raise ListenBrainzMissingTokenException

    def _is_token_valid(self) -> bool:
        return self.client.is_token_valid(self._token)

    def _set_token(self) -> None:
        self.client.set_auth_token(self._token, check_validity=True)

    def _get_listen_count(self) -> int:
        try:
            return self.client.get_user_listen_count(self._username)
        except ListenBrainzAPIException as e:
            if e.status_code == 404:
                raise ListenBrainzUnknownUserException

    def _get_playing_now(self) -> ListenBrainzListen | None:
        c: ListenBrainzListen = self.client.get_playing_now(self._username)
        if c is not None:
            info = c.additional_info
            if "duration_ms" in info:
                c.duration = round(info.get("duration_ms") / 1000)
            else:
                c.duration = info.get("duration", None)
            c.music_service = info.get("music_service", None)
        return c

    def _submit_listen(self, listen: Listen) -> any:
        return self.client.submit_single_listen(listen=listen)
