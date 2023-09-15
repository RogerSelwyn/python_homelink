"""HomeLINK test script."""
import asyncio

import bash_const
from pyhomelink.homelink import HomeLINK

CLIENTID = bash_const.HL_CLIENTID
CLIENTSECRET = bash_const.HL_CLIENTSECRET
# CLIENTSECRET = "blah"

HTTP_TIMEOUT = 6
RESPONSE_OK = 200
HEADERS = None
AUTHURL = (
    f"https://auth.live.homelync.io/oauth2?client={CLIENTID}&secret={CLIENTSECRET}"
)


async def main(access_token):
    """Run the main test process."""

    homelink = HomeLINK(
        access_token=access_token,
    )
    auth = await homelink.auth(
        clientid=CLIENTID,
        clientsecret=CLIENTSECRET,
    )
    print(f"Auth: {auth}")
    properties = await homelink.get_properties()

    for hl_property in properties:
        devices = await hl_property.get_devices()
        for device in devices:
            alerts = await device.get_alerts()
            print(
                f"Device {device.serialnumber} - {device.location}. Alerts:- {alerts}"
            )
        alerts = await hl_property.get_alerts()
        print(f"Property alerts:- {alerts}")

    hl_property = await homelink.get_property(properties[0].reference)
    print(f"Property: {hl_property.address}")
    devices = await homelink.get_property_devices(properties[0].reference)
    print(f"Property Devices: {hl_property.address} - {devices}")
    alerts = await homelink.get_property_alerts(properties[0].reference)
    print(f"Property Alerts: {hl_property.address} - {alerts}")
    tags = ["PROPERTY_JUNK"]
    tagso = await homelink.add_property_tags(properties[0].reference, tags)
    print(f"Property Add tags: {hl_property.address} - {tagso}")
    tagso = await homelink.delete_property_tags(properties[0].reference, tags)
    print(f"Property Delete tags: {hl_property.address} - {tagso}")

    devices = await homelink.get_devices()
    device = await homelink.get_device(devices[0].serialnumber)
    print(f"Device: {device.location}")
    alerts = await homelink.get_device_alerts(devices[0].serialnumber)
    print(f"Device Alerts: {device.location} - {alerts}")

    # alert = await landlord.get_alert("blah")
    # print(f"Alert: {alert}")

    lookups = await homelink.get_lookups("model")
    print(f"Lookups: 'model' - {lookups}")
    lookup = await homelink.get_lookup("model", lookups[0].lookupid)
    print(f"Lookup: 'model[0]' - {lookup.name}")

    tags = ["JUNK"]
    tagso = await hl_property.add_tags(tags)
    print(f"Add Tags: {tagso}")
    tags = ["JUNK"]
    tagso = await hl_property.delete_tags(tags)
    print(f"Add Tags: {tagso}")

    await homelink.api.session.close()


# response = requests.get(
#     AUTHURL,
#     timeout=HTTP_TIMEOUT,
#     headers=HEADERS,
# )
# if response.status_code == RESPONSE_OK:
# asyncio.run(main(response.json()["accessToken"]))
asyncio.run(main(None))
# else:
#     print("error")
