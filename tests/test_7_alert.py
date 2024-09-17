"""Test the HomeLINK property methods."""

from datetime import datetime

from pyhomelink.alert import Alert
from pyhomelink.api import HomeLINKApi

from .helpers.const import DEVICE_SERIAL, PROPERTY_REF
from .helpers.utils import create_mock


async def test_property_alerts(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}/alerts", "property_alerts.json")
    alerts = await homelink_api.async_get_property_alerts(PROPERTY_REF)

    alert = alerts[0]
    assert isinstance(alert, Alert)
    assert alert.alertid == "5f564e4f-2a47-431f-a470-134312f597fc"
    assert alert.serialnumber is None
    assert isinstance(alert.description, str)
    assert alert.eventtype == "AIRQUALITY_MEDIUM"
    assert alert.propertyreference == PROPERTY_REF
    assert alert.model == "AIRQUALITY"
    assert alert.modeltype == "INSIGHT"
    assert alert.location is None
    assert alert.locationnickname is None
    assert alert.insightid == "545e0647-84dc-11ee-a965-0a9f836b4814"
    assert isinstance(alert.raiseddate, datetime)
    assert alert.severity == "MEDIUM"
    assert alert.category == "INSIGHT"
    assert alert.hl_type == "INSIGHT"
    assert alert.status == "ACTIVE"
    assert alert.rel.hl_property == f"property/{PROPERTY_REF}"
    assert alert.rel.self == f"alert/{alert.alertid}"
    assert alert.rel.insight == f"insight/{alert.insightid}"


async def test_device_alerts(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL}/alerts", "device_alerts.json")
    alerts = await homelink_api.async_get_device_alerts(DEVICE_SERIAL)

    alert = alerts[0]
    assert isinstance(alert, Alert)
    assert alert.alertid == "d86fa724-a982-4980-88d9-9fa5e4c57d0d"
    assert alert.serialnumber == "001FD75F"
    assert isinstance(alert.description, str)
    assert alert.eventtype == "HEAD_REMOVED"
    assert alert.propertyreference == PROPERTY_REF
    assert alert.model == "Ei1025"
    assert alert.modeltype == "ENVCO2SENSOR"
    assert alert.location == "HALLWAY1"
    assert alert.locationnickname is None
    assert alert.insightid is None
    assert isinstance(alert.raiseddate, datetime)
    assert alert.severity == "MEDIUM"
    assert alert.category == "PRIORITY_MAINTENANCE"
    assert alert.hl_type == "DEVICE"
    assert alert.status == "ACTIVE"
    assert alert.rel.hl_property == f"property/{PROPERTY_REF}"
    assert alert.rel.self == f"alert/{alert.alertid}"
    assert not hasattr(alert.rel, "insight")
