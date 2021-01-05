from django.contrib import admin
from device.models import Vendor, DeviceType, Device, DeviceSample, DeviceSampleAccount

admin.site.register(Vendor)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(DeviceSample)
admin.site.register(DeviceSampleAccount)
