"""Test the HomeLINK property methods."""

from datetime import date, datetime

from pyhomelink.api import HomeLINKApi
from pyhomelink.property import Property
from pyhomelink.reading import PropertyReading

from .helpers.const import PROPERTY_REF
from .helpers.utils import create_mock, create_update_mock


async def test_properties(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test properties request."""

    create_mock(mock_aio, "/property", "properties.json")

    properties = await homelink_api.async_get_properties()

    assert len(properties) == 1
    hl_property = properties[0]
    assert isinstance(hl_property, Property)
    assert hl_property.reference == PROPERTY_REF
    assert isinstance(hl_property.createdate, datetime)
    assert isinstance(hl_property.updatedat, datetime)
    assert hl_property.postcode == "PostCode"
    assert hl_property.latitude == 60.01953704
    assert hl_property.longitude == 1.36647542
    assert hl_property.address == "My House Town City County PostCode GB"
    assert hl_property.tags == ["COTTAGE"]
    assert hl_property.rel.self == f"property/{PROPERTY_REF}"


async def test_properties_2(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test properties (x2) request."""

    create_mock(mock_aio, "/property", "propertiesx2.json")
    properties = await homelink_api.async_get_properties()

    assert len(properties) == 2


async def test_property(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}", "property.json")
    hl_property = await homelink_api.async_get_property(PROPERTY_REF)

    assert hl_property.reference == PROPERTY_REF


async def test_property_get_devices(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property devices request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}", "property.json")
    hl_property = await homelink_api.async_get_property(PROPERTY_REF)

    create_mock(mock_aio, f"/property/{PROPERTY_REF}/devices", "property_devices.json")
    devices = await hl_property.async_get_devices()

    assert len(devices) == 7


async def test_property_devices(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property devices request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}/devices", "property_devices.json")
    devices = await homelink_api.async_get_property_devices(PROPERTY_REF)

    assert len(devices) == 7


async def test_property_get_insights(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property insights request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}", "property.json")
    hl_property = await homelink_api.async_get_property(PROPERTY_REF)

    create_mock(
        mock_aio, f"/property/{PROPERTY_REF}/insights", "property_insights.json"
    )
    insights = await hl_property.async_get_insights()

    assert len(insights) == 14


async def test_property_insights(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property insights request."""

    create_mock(
        mock_aio, f"/property/{PROPERTY_REF}/insights", "property_insights.json"
    )
    insights = await homelink_api.async_get_property_insights(PROPERTY_REF)

    assert len(insights) == 14


async def test_property_get_alerts(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}", "property.json")
    hl_property = await homelink_api.async_get_property(PROPERTY_REF)

    create_mock(mock_aio, f"/property/{PROPERTY_REF}/alerts", "property_alerts.json")
    alerts = await hl_property.async_get_alerts()

    assert len(alerts) == 4


async def test_property_alerts(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}/alerts", "property_alerts.json")
    alerts = await homelink_api.async_get_property_alerts(PROPERTY_REF)

    assert len(alerts) == 4


async def test_property_get_readings(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}", "property.json")
    hl_property = await homelink_api.async_get_property(PROPERTY_REF)

    create_mock(
        mock_aio,
        f"/property/{PROPERTY_REF}/readings?date={date.today()}",
        "property_readings.json",
    )
    readings = await hl_property.async_get_readings(date.today())

    assert len(readings) == 4

    reading = readings[0]
    assert isinstance(reading, PropertyReading)
    assert reading.unit == "ppm"
    assert reading.type == "environment-co2-indoor"
    assert isinstance(reading.dataavailability, str)
    assert len(reading.devices) == 1

    readingdevice = reading.devices[0]
    assert readingdevice.serialnumber == "C3CEC7FB-001FD75F"
    assert readingdevice.rel.hl_property == f"property/{PROPERTY_REF}"
    assert readingdevice.rel.device == f"device/{readingdevice.serialnumber}"
    assert len(readingdevice.values) == readingdevice.count

    readingvalue = readingdevice.values[0]
    assert readingvalue.value == 1235
    assert isinstance(readingvalue.readingdate, datetime)


async def test_property_readings(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_mock(
        mock_aio,
        f"/property/{PROPERTY_REF}/readings?date={date.today()}",
        "property_readings.json",
    )
    readings = await homelink_api.async_get_property_readings(
        PROPERTY_REF, date.today()
    )

    assert len(readings) == 4


async def test_property_get_add_tag(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}", "property.json")
    hl_property = await homelink_api.async_get_property(PROPERTY_REF)
    assert hl_property.tags == ["COTTAGE"]

    create_update_mock(
        mock_aio,
        "put",
        f"/property/{PROPERTY_REF}/tags",
        "property_tags_add.json",
    )
    newtag = "NEWTAG"
    tags = [newtag]
    tags = await hl_property.async_add_tags(tags)

    assert tags["tags"] == ["COTTAGE", newtag]


async def test_property_add_tag(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_update_mock(
        mock_aio,
        "put",
        f"/property/{PROPERTY_REF}/tags",
        "property_tags_add.json",
    )
    newtag = "NEWTAG"
    tags = [newtag]
    tags = await homelink_api.async_add_property_tags(PROPERTY_REF, tags)

    assert tags["tags"] == ["COTTAGE", newtag]


async def test_property_get_delete_tag(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}", "property.json")
    hl_property = await homelink_api.async_get_property(PROPERTY_REF)
    assert hl_property.tags == ["COTTAGE"]

    create_update_mock(
        mock_aio,
        "delete",
        f"/property/{PROPERTY_REF}/tags",
        "property_tags_delete.json",
    )
    deltag = "COTTAGE"
    tags = [deltag]
    tags = await hl_property.async_delete_tags(tags)

    assert tags["tags"] == []


async def test_property_delete_tag(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_update_mock(
        mock_aio,
        "delete",
        f"/property/{PROPERTY_REF}/tags",
        "property_tags_delete.json",
    )
    deltag = "COTTAGE"
    tags = [deltag]
    tags = await homelink_api.async_delete_property_tags(PROPERTY_REF, tags)

    assert tags["tags"] == []
