"""Test the HomeLINK reading methods."""

from datetime import date, datetime

from pyhomelink.api import HomeLINKApi
from pyhomelink.const import HomeLINKReadingType
from pyhomelink.device import DeviceReading
from pyhomelink.reading import PropertyReading

from .helpers.const import DEVICE_SERIAL, PROPERTY_REF
from .helpers.utils import create_mock


async def test_property_readings(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test property alerts request."""

    create_mock(mock_aio, f"/property/{PROPERTY_REF}", "property.json")
    hl_property = await homelink_api.async_get_property(PROPERTY_REF)

    create_mock(
        mock_aio,
        f"/property/{PROPERTY_REF}/readings?date={date.today()}",
        "property_readings.json",
    )
    readings = await hl_property.async_get_readings(date.today())

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


async def test_device_readings_start(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    today = date.today()
    create_mock(
        mock_aio,
        f"/device/{DEVICE_SERIAL}/readings/environment-temperature-indoor?start={today}",
        "device_readings_temp.json",
    )
    reading = await homelink_api.async_get_device_readings(
        DEVICE_SERIAL, HomeLINKReadingType.TEMPERATURE, start=today
    )
    assert isinstance(reading, DeviceReading)
    assert reading.unit == "celsius"
    assert reading.type == "environment-temperature-indoor"
    assert isinstance(reading.dataavailability, str)
    assert reading.rel.hl_property == f"property/{PROPERTY_REF}"
    assert reading.rel.device == f"device/{DEVICE_SERIAL}"
    assert len(reading.values) == reading.count

    readingvalue = reading.values[0]
    assert readingvalue.value == 20.31
    assert readingvalue.serialnumber == "C3CEC7FB-001FD799"
    assert readingvalue.readingtypeid == "environment.temperature.indoor"
    assert readingvalue.statusid == "ACTIVE"
    assert isinstance(readingvalue.readingdate, datetime)
