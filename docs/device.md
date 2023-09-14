---
title: Device
nav_order: 3
---

# Device

## Get Devices

```
devices = await homelink.get_devices()
```

## Get Device

```
device = await homelink.get_devices(serialnumber)
```

## Get Device Alerts

```
alerts = await homelink.get_device_alerts(serialnumber)
```

or if device has already been retrieved

``` 
alerts = await device.get_alerts()
```
