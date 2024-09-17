"""Test the HomeLINK property methods."""

from unittest.mock import Mock, patch

import pytest
from aiohttp import ClientError, ClientResponseError

from pyhomelink.api import HomeLINKApi
from pyhomelink.exceptions import ApiException, AuthException
from pyhomelink.version import __version__

from .conftest import ApiAuthImpl
from .helpers.utils import create_mock


async def test_version():
    """Test the version."""
    assert isinstance(__version__, str)


async def test_token_retrieval(homelink_api_unauth: HomeLINKApi, mock_aio) -> None:
    """Test base property request."""

    new_token = "longtoken"
    mock_aio.get(
        "https://auth.live.homelync.io/oauth2?client=1234&secret=5678",
        status=200,
        body='{"accessToken": "%s"}' % (new_token),
    )
    token = await homelink_api_unauth.auth.async_get_access_token()
    assert token == new_token


async def test_credential_rejection(homelink_api_unauth: HomeLINKApi, mock_aio) -> None:
    """Test base property request."""

    new_token = "longtoken"
    mock_aio.get(
        "https://auth.live.homelync.io/oauth2?client=1234&secret=5678",
        status=401,
        body='{"accessToken": "%s"}' % (new_token),
    )
    with pytest.raises(ClientResponseError):
        await homelink_api_unauth.auth.async_get_access_token()


async def test_401(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test 401 error."""

    create_mock(mock_aio, "/property", "properties.json", status=401)
    with pytest.raises(AuthException):
        await homelink_api.async_get_properties()


async def test_500(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test none 401 error."""

    create_mock(mock_aio, "/property", "properties.json", status=500)
    with pytest.raises(ApiException):
        await homelink_api.async_get_properties()


@patch.multiple(
    ApiAuthImpl,
    __abstractmethods__=set(),
    async_get_access_token=Mock(side_effect=ClientError()),
)
async def test_clienterror(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test none 401 error."""

    create_mock(mock_aio, "/property", "properties.json")
    with pytest.raises(RuntimeError):
        await homelink_api.async_get_properties()
