"""Adds config flow for listenbrainz."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN, CONF_USERNAME
from homeassistant.helpers import selector

from liblistenbrainz.errors import ListenBrainzAPIException

from .api import (
    ListenBrainzApiClient,
    ListenBrainzInvalidTokenException,
    ListenBrainzUnknownUserException,
)
from .const import DOMAIN, LOGGER


class ListenBrainzFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for listenbrainz."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    username=user_input[CONF_USERNAME],
                    token=user_input.get(CONF_API_TOKEN, None),
                )
            except ListenBrainzUnknownUserException:
                LOGGER.warning("Could not complete setup: User '%s' does not exist", user_input[CONF_USERNAME])
                _errors[CONF_USERNAME] = "unknown_user"
            except ListenBrainzInvalidTokenException:
                LOGGER.warning("Could not complete setup: Invalid token")
                _errors[CONF_API_TOKEN] = "invalid_token"
            except ListenBrainzAPIException as e:
                LOGGER.exception(e)
                _errors["base"] = "api"
            else:
                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Optional(CONF_API_TOKEN): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_credentials(self, username: str, token: str | None) -> None:
        """Validate credentials."""
        client = ListenBrainzApiClient(
            hass=self.hass,
            username=username,
            token=token,
        )
        await client.validate_input()
