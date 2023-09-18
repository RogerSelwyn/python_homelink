"""HomeLINK test script."""
import asyncio
import sys
from typing import cast

import aiohttp
from aiohttp import ClientSession

import bash_const
from pyhomelink.api import HomeLINKApi
from pyhomelink.auth import AbstractAuth

CLIENTID = bash_const.HL_CLIENTID
CLIENTSECRET = bash_const.HL_CLIENTSECRET


class ApiAuthImpl(AbstractAuth):
    """Authentication implementation for HomeLINK api library."""

    def __init__(
        self,
        websession: aiohttp.ClientSession,
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


async def _test():
    async with ClientSession() as session:
        homelink_api = HomeLINKApi(ApiAuthImpl(session, ""))
        properties = await homelink_api.async_get_properties()
        print(f"Properties: {properties[0].reference}")

        for hl_property in properties:
            devices = await hl_property.async_get_devices()
            for device in devices:
                alerts = await device.async_get_alerts()
                print(
                    f"Device: {device.serialnumber} - {device.location}. Alerts:- {alerts}"
                )
            alerts = await hl_property.async_get_alerts()
            print(f"Property alerts: {hl_property.reference}. Alerts:- {alerts}")

        hl_property = await homelink_api.async_get_property(properties[0].reference)
        print(f"Property: {hl_property.address}")
        devices = await homelink_api.async_get_property_devices(hl_property.reference)
        print(f"Property Devices: {hl_property.address} - {devices[0].serialnumber}")
        alerts = await homelink_api.async_get_property_alerts(properties[0].reference)
        print(f"Property Alerts: {hl_property.address} - {alerts}")

        tags = ["PROPERTY_JUNK"]
        tagso = await homelink_api.async_add_property_tags(hl_property.reference, tags)
        print(f"Property Add tags: {hl_property.address} - {tagso}")
        tagso = await homelink_api.async_delete_property_tags(
            hl_property.reference, tags
        )
        print(f"Property Delete tags: {hl_property.address} - {tagso}")
        tags = ["JUNK"]
        tagso = await hl_property.async_add_tags(tags)
        print(f"Add Tags: {tagso}")
        tags = ["JUNK"]
        tagso = await hl_property.async_delete_tags(tags)
        print(f"Add Tags: {tagso}")

        devices = await homelink_api.async_get_devices()
        print(f"Devices: {devices[0].serialnumber}")
        device = await homelink_api.async_get_device(devices[0].serialnumber)
        print(f"Device: {device.serialnumber}")
        alerts = await homelink_api.async_get_device_alerts(device.serialnumber)
        print(f"Device Alerts: {device.location} - {alerts}")

        lookups = await homelink_api.async_get_lookups("model")
        print(f"Lookups: 'model' - {lookups[0].code}")
        lookup = await homelink_api.async_get_lookup("model", lookups[0].lookupid)
        print(f"Lookup: 'model[0]' - {lookup.name}")

        print("Success", file=sys.stdout)


async def main():
    """Main."""
    print("start\n", file=sys.stdout)
    await _test()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
