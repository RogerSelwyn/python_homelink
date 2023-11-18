---
title: Device
nav_order: 3
---

# Device

## Get Devices

```
devices = await homelink_api.async_get_devices()
```

## Get Device

```
device = await homelink_api.async_get_devices(serialnumber)
```

## Get Device Alerts

```
alerts = await homelink_api.async_get_device_alerts(serialnumber)
```

or if device has already been retrieved

``` 
alerts = await device.async_get_alerts()
```

## Get Device Readings

```
readings = await homelink_api.async_get_device_readings(serialnumber, readingtype, start, end)
```

or if property has already been retrieved

``` 
readings = await property.async_get_readings(readingtype, start, end)
```

Start/End are optional and in the format `YYYY-MM-DD` e.g. 2023-11-18