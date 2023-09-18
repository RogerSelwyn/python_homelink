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
