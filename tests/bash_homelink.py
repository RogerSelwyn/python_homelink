"""HomeLINK test script."""
import asyncio
import sys

import aiohttp
import requests

sys.path.append("/HADev/Hassio/dev-config")
import const

from pyhomelink.landlord import Landlord

CLIENTID = const.HL_CLIENTID
CLIENTSECRET = const.HL_CLIENTSECRET


HTTP_TIMEOUT = 6
RESPONSE_OK = 200
HEADERS = None
AUTHURL = (
    f"https://auth.live.homelync.io/oauth2?client={CLIENTID}&secret={CLIENTSECRET}"
)


async def main(access_token):
    """Run the main test process."""
    async with aiohttp.ClientSession() as session:
        landlord = Landlord(
            websession=session,
            access_token=access_token,
            # clientid=CLIENTID,
            # clientsecret=CLIENTSECRET,
        )

        properties = await landlord.get_properties()

        for hl_property in properties:
            devices = await hl_property.get_devices()
            for device in devices:
                alerts = await device.get_alerts()
                print(
                    f"Device {device.serialnumber} - {device.location}. Alerts:- {alerts}"
                )
            alerts = await hl_property.get_alerts()
            print(f"Property alerts:- {alerts}")

        hl_property = await landlord.get_property(properties[0].reference)
        print(f"Property: {hl_property.address}")
        devices = await landlord.get_property_devices(properties[0].reference)
        print(f"Property Devices: {hl_property.address} - {devices}")
        alerts = await landlord.get_property_alerts(properties[0].reference)
        print(f"Property Alerts: {hl_property.address} - {alerts}")

        devices = await landlord.get_devices()
        device = await landlord.get_device(devices[0].serialnumber)
        print(f"Device: {device.location}")
        alerts = await landlord.get_device_alerts(devices[0].serialnumber)
        print(f"Device Alerts: {device.location} - {alerts}")

        # alert = await landlord.get_alert("blah")
        # print(f"Alert: {alert}")


response = requests.get(
    AUTHURL,
    timeout=HTTP_TIMEOUT,
    headers=HEADERS,
)
if response.status_code == RESPONSE_OK:
    asyncio.run(main(response.json()["accessToken"]))
else:
    print("error")
