from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from device.models import DeviceType
import os


class TechReq(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=500)
    desc = models.CharField(max_length=3000, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='tech_req_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='tech_req_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class TechReqFile(models.Model):
    tech_req = models.ForeignKey(TechReq, related_name='tech_req_file', on_delete=models.CASCADE)
    file = models.FileField(upload_to="tech_req/files/")
    desc = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='tech_req_file_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='tech_req_file_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def filename(self):
        return os.path.basename(self.file.name)
