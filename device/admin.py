from django.contrib import admin
from device.models import Device, DeviceType

# Register your models here.

admin.site.register(Device)
admin.site.register(DeviceType)
