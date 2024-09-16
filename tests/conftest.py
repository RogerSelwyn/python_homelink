# pylint: disable=protected-access,redefined-outer-name
"""Global fixtures for library."""

from typing import cast

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from pyhomelink.api import HomeLINKApi
from pyhomelink.auth import AbstractAuth

from .helpers.const import CLIENTID, CLIENTSECRET


class ApiAuthImpl(AbstractAuth):
    """Authentication implementation for HomeLINK api library."""

    def __init__(
        self,
        websession: ClientSession,
        token,
    ) -> None:
        """Init the HomeLINK client library auth implementation."""
        super().__init__(websession)
        self._token = token

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        url = f"?client={CLIENTID}&secret={CLIENTSECRET}"
        resp = await self.async_get_token(url)
        resp.raise_for_status()
        self._token = cast(dict, await resp.json())
        return cast(str, self._token["accessToken"])


@pytest.fixture
async def aiohttp_client_session():
    """Create the client session."""
    async with ClientSession() as session:
        yield session


@pytest.fixture
def mock_aio():
    """Mock AIO calls."""
    with aioresponses() as m:
        yield m


@pytest.fixture
async def homelink_api_unauth(aiohttp_client_session: ClientSession) -> HomeLINKApi:
    """Homelinkapi."""

    return HomeLINKApi(ApiAuthImpl(aiohttp_client_session, ""))


@pytest.fixture
async def homelink_api(homelink_api_unauth, mock_aio) -> HomeLINKApi:
    """Homelink authenticated api."""

    new_token = "longtoken"
    mock_aio.get(
        "https://auth.live.homelync.io/oauth2?client=1234&secret=5678",
        status=200,
        body='{"accessToken": "%s"}' % (new_token),
        repeat=True,
    )
    return homelink_api_unauth
