from django.db import models
from device.models import Device
from testplan.models import TestPlan, Test
from datetime import datetime


class Protocol(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    testplan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    sw = models.CharField(max_length=50)
    sw_checksum = models.CharField(max_length=50, blank=True, null=True)
    engineer_login = models.CharField(max_length=50, blank=True, null=True)
    engineer_password = models.CharField(max_length=50, blank=True, null=True)
    sysinfo = models.TextField(blank=True, null=True)
    console = models.TextField(blank=True, null=True)
    date_of_start = models.DateField(default=datetime.now, blank=True)
    date_of_finish = models.DateField(default=datetime.now, blank=True)


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    result = models.IntegerField()
    config = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
