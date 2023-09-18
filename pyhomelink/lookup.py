"""Python module for accessing HomeLINK Lookup."""
# import logging


from .auth import AbstractAuth


class Lookup:
    """Lookup is the instantiation of a HomeLINK Lookup"""

    def __init__(self, raw_data: dict, auth: AbstractAuth):
        """Initialize the property."""
        # super().__init__(
        #     parent
        # )
        self._raw_data = raw_data
        self._auth = auth

    @property
    def lookupid(self) -> str:
        """Return the id of the Lookup"""
        return self._raw_data["id"]

    @property
    def code(self) -> str:
        """Return the codet of the Lookup"""
        return self._raw_data["code"]

    @property
    def name(self) -> str:
        """Return the name of the Lookup"""
        return self._raw_data["name"]

    @property
    def description(self) -> str:
        """Return the descriptionof the Lookup"""
        return self._raw_data["description"]

    @property
    def active(self) -> bool:
        """Return the active of the Lookup"""
        return self._raw_data["active"]

    # async def async_get_devices(self) -> List[Device]:
    #     """Return the Devices."""
    #     resp = await self._auth.request("get", f"{self.rel.devices}")
    #     resp.raise_for_status()
    #     return [
    #         Device(device_data, self._auth)
    #         for device_data in (await resp.json())["results"]
    #     ]
