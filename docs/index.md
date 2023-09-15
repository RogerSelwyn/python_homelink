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

```
from pyhomelink.homelink import HomeLINK
homelink = HomeLINK()
```
Optional parameters:
* session - An async session (for instance the Home Assistant websession)
* access_token - a JWT access token previously obtained

## Access token retrieval

```
access_token = homelink.auth(clientid, clientsecret)
```
