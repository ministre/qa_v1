from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from device.models import Device
from testplan.models import TestPlan, Test


class Protocol(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    testplan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    sw = models.CharField(max_length=50)
    sw_checksum = models.CharField(max_length=50, blank=True, null=True)
    engineer_login = models.CharField(max_length=50, blank=True, null=True)
    engineer_password = models.CharField(max_length=200, blank=True, null=True)
    sysinfo = models.TextField(blank=True, null=True)
    console = models.TextField(blank=True, null=True)
    date_of_start = models.DateField(default=timezone.now)
    date_of_finish = models.DateField(default=timezone.now, blank=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='protocol_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='protocol_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    result = models.IntegerField(default=0)

    def __str__(self):
        name = 'ID: ' + str(self.id)
        if self.sw:
            name += ' / SW Ver.: ' + str(self.sw)
        if self.date_of_start:
            name += ' / Date of testing: ' + str(self.date_of_start.strftime('%d.%m.%Y'))
        if self.date_of_finish:
            name += ' - ' + str(self.date_of_finish.strftime('%d.%m.%Y'))
        return name


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    result = models.IntegerField()
    config = models.TextField(default=None, blank=True, null=True)
    info = models.TextField(default=None, blank=True, null=True)
    comment = models.TextField(default=None, blank=True, null=True)
