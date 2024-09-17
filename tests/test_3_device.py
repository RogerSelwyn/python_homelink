"""Test the HomeLINK property methods."""

from datetime import date, datetime, timedelta

from pyhomelink.api import HomeLINKApi
from pyhomelink.const import HomeLINKReadingType
from pyhomelink.device import Device, DeviceReading

from .helpers.const import DEVICE_SERIAL, DEVICE_SERIAL_CO2, PROPERTY_REF
from .helpers.utils import create_mock


async def test_devices(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test devices request."""

    create_mock(mock_aio, "/device", "devices.json")

    devices = await homelink_api.async_get_devices()

    assert len(devices) == 7
    device = devices[0]
    assert isinstance(device, Device)
    assert device.serialnumber == "D8EAF0D0"
    assert device.model == "Ei3016"
    assert device.modeltype == "FIREALARM"
    assert device.location == "LIVINGROOM"
    assert device.locationnickname is None
    assert device.manufacturer == "Ei"
    assert isinstance(device.installationdate, datetime)
    assert device.installedby == "Dummy User"
    assert isinstance(device.replacedate, datetime)
    assert isinstance(device.createdat, datetime)
    assert isinstance(device.updatedat, datetime)
    assert device.metadata.signalstrength == -50
    assert isinstance(device.metadata.lastseendate, datetime)
    assert device.metadata.connectivitytype == "EIRF868"
    assert device.status.operationalstatus == "GOOD"
    assert isinstance(device.status.lasttesteddate, datetime)
    assert device.status.datacollectionstatus == "ACTIVE"
    assert device.rel.self == "device/D8EAF0D0"
    assert device.rel.hl_property == f"property/{PROPERTY_REF}"
    assert not hasattr(device.rel, "readings")


async def test_device(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test devices request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL}", "device.json")

    device = await homelink_api.async_get_device(DEVICE_SERIAL)

    assert device.serialnumber == DEVICE_SERIAL
    assert not hasattr(device.rel.readings, "co2readings")


async def test_device_co2(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test devices request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL_CO2}", "device_co2.json")

    device = await homelink_api.async_get_device(DEVICE_SERIAL_CO2)

    assert device.serialnumber == DEVICE_SERIAL_CO2
    assert hasattr(device.rel.readings, "co2readings")


async def test_device_get_alerts(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL}", "device.json")
    device = await homelink_api.async_get_device(DEVICE_SERIAL)

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL}/alerts", "device_alerts.json")
    alerts = await device.async_get_alerts()

    assert len(alerts) == 1


async def test_device_alerts(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL}/alerts", "device_alerts.json")
    alerts = await homelink_api.async_get_device_alerts(DEVICE_SERIAL)

    assert len(alerts) == 1


async def test_device_get_readings_start(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL}", "device.json")
    device = await homelink_api.async_get_device(DEVICE_SERIAL)

    today = date.today()
    create_mock(
        mock_aio,
        f"/device/{DEVICE_SERIAL}/readings/environment-temperature-indoor?start={today}",
        "device_readings_temp.json",
    )
    reading = await device.async_get_device_readings(
        HomeLINKReadingType.TEMPERATURE, start=today
    )
    assert reading.unit == "celsius"


async def test_device_get_readings_start_end(
    homelink_api: HomeLINKApi, mock_aio
) -> None:
    """Test device alerts request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL}", "device.json")
    device = await homelink_api.async_get_device(DEVICE_SERIAL)

    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    create_mock(
        mock_aio,
        f"/device/{DEVICE_SERIAL}/readings/environment-temperature-indoor?start={yesterday}&end={today}",
        "device_readings_temp.json",
    )
    reading = await device.async_get_device_readings(
        HomeLINKReadingType.TEMPERATURE, start=yesterday, end=today
    )
    assert reading.unit == "celsius"


async def test_device_get_readings_end(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL}", "device.json")
    device = await homelink_api.async_get_device(DEVICE_SERIAL)

    today = date.today()
    create_mock(
        mock_aio,
        f"/device/{DEVICE_SERIAL}/readings/environment-temperature-indoor?end={today}",
        "device_readings_temp.json",
    )
    reading = await device.async_get_device_readings(
        HomeLINKReadingType.TEMPERATURE, end=today
    )
    assert reading.unit == "celsius"


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


async def test_device_readings_start_end(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    create_mock(
        mock_aio,
        f"/device/{DEVICE_SERIAL}/readings/environment-temperature-indoor?start={yesterday}&end={today}",
        "device_readings_temp.json",
    )
    reading = await homelink_api.async_get_device_readings(
        DEVICE_SERIAL, HomeLINKReadingType.TEMPERATURE, start=yesterday, end=today
    )
    assert reading.unit == "celsius"


async def test_device_readings_end(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    today = date.today()
    create_mock(
        mock_aio,
        f"/device/{DEVICE_SERIAL}/readings/environment-temperature-indoor?end={today}",
        "device_readings_temp.json",
    )
    reading = await homelink_api.async_get_device_readings(
        DEVICE_SERIAL, HomeLINKReadingType.TEMPERATURE, end=today
    )
    assert reading.unit == "celsius"


async def test_device_readings_co2(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL_CO2}", "device_co2.json")
    device = await homelink_api.async_get_device(DEVICE_SERIAL_CO2)

    today = date.today()
    create_mock(
        mock_aio,
        f"/device/{DEVICE_SERIAL_CO2}/readings/environment-co2-indoor?start={today}",
        "device_readings_co2.json",
    )
    reading = await device.async_get_device_readings(
        HomeLINKReadingType.CO2, start=today
    )
    assert reading.unit == "ppm"


async def test_device_readings_humidity(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test device alerts request."""

    create_mock(mock_aio, f"/device/{DEVICE_SERIAL_CO2}", "device_co2.json")
    device = await homelink_api.async_get_device(DEVICE_SERIAL_CO2)

    today = date.today()
    create_mock(
        mock_aio,
        f"/device/{DEVICE_SERIAL_CO2}/readings/environment-humidity-indoor?start={today}",
        "device_readings_humidity.json",
    )
    reading = await device.async_get_device_readings(
        HomeLINKReadingType.HUMIDITY, start=today
    )
    assert reading.unit == "rh %"
