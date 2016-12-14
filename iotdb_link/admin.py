from django.contrib import admin

from models import Device, DataFromDevice

class DataFromDeviceAdmin(admin.ModelAdmin):
    list_display = ('time', 'device', 'data')
    list_filter = ['time']

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'parking_slot')

# Register your models here.
admin.site.register(Device, DeviceAdmin)
admin.site.register(DataFromDevice, DataFromDeviceAdmin)
