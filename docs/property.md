---
title: Property
nav_order: 2
---

# Property

## Get Properties

```
properties = await homelink_api.async_get_properties()
```

## Get Property

```
devices = await homelink_api.async_get_property(propertyreference)
```

## Get Property Devices

```
devices = await homelink_api.async_get_property_devices(propertyreference)
```

or if property has already been retrieved

``` 
devices = await property.get_devices()
```

## Get Property Alerts

```
alerts = await homelink_api.async_get_property_alerts(propertyreference)
```

or if property has already been retrieved

``` 
alerts = await property.async_get_alerts()
```

## Add Property Tags

```
tags = {"tagsId": ["NEWTAG_1", "NEWTAG_2"]}
updated_tags = await homelink_api.async_add_property_tags(propertyreference, tags)
```

or if property has already been retrieved

``` 
tags = {"tagsId": ["NEWTAG_1", "NEWTAG_2"]}
updated_tags = await property.async_add_tags(tags)
```

## Delete Property Tags

```
tags = {"tagsId": ["DELTAG_1", "DELWTAG_2"]}
updated_tags = await homelink_api.async_delete_property_tags(propertyreference, tags)
```

or if property has already been retrieved

``` 
tags = {"tagsId": ["DELTAG_1", "DELTAG_2"]}
updated_tags = await property.async_delete_tags(tags)
```
