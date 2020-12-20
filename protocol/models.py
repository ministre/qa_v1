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
