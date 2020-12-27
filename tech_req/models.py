from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from device.models import DeviceType


class TechReq(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    desc = models.CharField(max_length=3000, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='tech_req_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='tech_req_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
