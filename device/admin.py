from django.contrib import admin
from device.models import Vendor, DeviceType, Device, DevicePhoto, DeviceSample, DeviceSampleAccount, DeviceFile, \
    DeviceNote

admin.site.register(Vendor)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(DevicePhoto)
admin.site.register(DeviceSample)
admin.site.register(DeviceSampleAccount)
admin.site.register(DeviceFile)
admin.site.register(DeviceNote)
