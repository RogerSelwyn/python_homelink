"""Test the HomeLINK property methods."""

from pyhomelink.api import HomeLINKApi
from pyhomelink.const import LOOKUPEVENTTYPE
from pyhomelink.lookup import Lookup, LookupEventType

from .helpers.const import LOOKUP_ID
from .helpers.utils import create_mock


async def test_lookups_eventtype(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test lookups request."""

    create_mock(mock_aio, f"/lookup/{LOOKUPEVENTTYPE}", "lookups_eventtype.json")

    lookups = await homelink_api.async_get_lookups(LOOKUPEVENTTYPE)

    assert len(lookups) == 91
    lookup = lookups[0]
    assert isinstance(lookup, LookupEventType)
    assert lookup.lookupid == "ABANDONMENT_RISK_HIGH"
    assert lookup.code == "ABANDONMENT_RISK_HIGH"
    assert lookup.name == "Void Risk High"
    assert lookup.description == "This property is at high risk of being void"
    assert lookup.eventcategoryid == "INSIGHT"
    assert lookup.severityid == "HIGH"
    assert lookup.active is True


async def test_lookups_location(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test lookups request."""

    create_mock(mock_aio, "/lookup/location", "lookups_location.json")

    lookups = await homelink_api.async_get_lookups("location")

    assert len(lookups) == 38
    lookup = lookups[0]
    assert isinstance(lookup, Lookup)
    assert not hasattr(lookup, "eventcategoryid")
    assert not hasattr(lookup, "severityid")


async def test_lookup(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test lookups request."""

    create_mock(mock_aio, f"/lookup/{LOOKUPEVENTTYPE}/{LOOKUP_ID}", "lookup.json")

    lookup = await homelink_api.async_get_lookup(LOOKUPEVENTTYPE, LOOKUP_ID)

    assert lookup.lookupid == LOOKUP_ID
    assert isinstance(lookup, LookupEventType)
