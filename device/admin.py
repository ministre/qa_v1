from django.contrib import admin
from device.models import Vendor, DeviceType, Device


admin.site.register(Vendor)
admin.site.register(DeviceType)
admin.site.register(Device)
