"""Test the HomeLINK property methods."""

import pytest
from aiohttp import ClientResponseError

from pyhomelink.api import HomeLINKApi


async def test_token_retrieval(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test base property request."""

    new_token = "longtoken"
    mock_aio.get(
        "https://auth.live.homelync.io/oauth2?client=1234&secret=5678",
        status=200,
        body='{"accessToken": "%s"}' % (new_token),
    )
    token = await homelink_api.auth.async_get_access_token()
    assert token == new_token


async def test_credential_rejection(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test base property request."""

    new_token = "longtoken"
    mock_aio.get(
        "https://auth.live.homelync.io/oauth2?client=1234&secret=5678",
        status=401,
        body='{"accessToken": "%s"}' % (new_token),
    )
    with pytest.raises(ClientResponseError):
        await homelink_api.auth.async_get_access_token()


# async def test_token_retrieval(homelink_api: HomeLINKApi, mock_aio) -> None:
#     """Test base property request."""

#     mock_aio.get(
#         "https://auth.live.homelync.io/oauth2?client=1234&secret=5678",
#         status=200,
#         body='{"accessToken": "longtoken"}',
#     )
#     properties = await homelink_api.async_get_properties()
