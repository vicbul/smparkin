from SmartParking import settings

if settings.CHECK_MQTT_SERVER is True:
    import mqtt_sub
    mqtt_sub.connect()