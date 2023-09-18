---
title: Home
nav_order: 1
---

# python_homelink
Python module for accessing AICO HomeLINK services.

## Introduction

This library enables access to the AICO HomeLINK api for retrieving the following items:
* Property
* Devices
* Alerts
* Lookups

HomeLINK swagger docs from which this module has been built, can be found here - https://frontier.live.homelync.io/api-docs/. The outputs form each call is as documented in the swagger documents, except that they are returned as a python object and some minor field name changes.

## Installing

To install:

```
pip install pyhomelink
```

## Usage

This library implements AbstractAuth as such, fetching the token is up to you, though this library implements a method `async_get_token` to enable you to pass a Client ID and secret and fetch a token. Note that at time of writing the token is valid for 24 hours. The Library does not store any credentials.

You need to implement AbstractAuth (see bash_homelink.py in tests) with an async_get_access_token method, which constructs the url suffix and retrieves the token

```
from pyhomelink.api import HomeLINKApi
homelink_api = HomeLINKApi(ApiAuthImpl(session, ""))
```
## Access token retrieval

```
    url = f"?client={CLIENTID}&secret={CLIENTSECRET}"
    resp = await self.async_get_token(url)
    self._token = cast(dict, await resp.json())
    return cast(str, self._token["accessToken"])
```
