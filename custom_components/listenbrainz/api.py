"""Sample API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class ListenBrainzApiClientError(Exception):
    """Exception to indicate a general API error."""


class ListenBrainzApiClientCommunicationError(
    ListenBrainzApiClientError
):
    """Exception to indicate a communication error."""


class ListenBrainzApiClientAuthenticationError(
    ListenBrainzApiClientError
):
    """Exception to indicate an authentication error."""


class ListenBrainzApiClient:
    """Sample API Client."""

    def __init__(
        self,
        username: str,
        token: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._token = token
        self._session = session

    async def validate_token(self) -> any:
        """Validate Token"""
        return await self._api_wrapper(
            method="get", url="https://api.listenbrainz.org/1/validate-token", headers={"Authorization": f"Token {self._token}"}
        )

    async def async_get_data(self) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get", url="https://jsonplaceholder.typicode.com/posts/1"
        )

    async def async_set_title(self, value: str) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (400, 401, 403):
                    raise ListenBrainzApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise ListenBrainzApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ListenBrainzApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ListenBrainzApiClientError(
                "Something really wrong happened!"
            ) from exception
