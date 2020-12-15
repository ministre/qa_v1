from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DeviceType(models.Model):
    name = models.CharField(max_length=300)
    redmine_project = models.CharField(max_length=100, blank=True, null=True)
    redmine_project_name = models.CharField(max_length=1000, blank=True, null=True)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    main_type = models.CharField(max_length=50, blank=True, null=True)
    sub_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Device(models.Model):
    project_id = models.CharField(max_length=50)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    vendor = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    hw = models.CharField(max_length=50, blank=True, null=True)
    interfaces = models.CharField(max_length=300, blank=True, null=True)
    leds = models.CharField(max_length=300, blank=True, null=True)
    buttons = models.CharField(max_length=300, blank=True, null=True)
    chipsets = models.CharField(max_length=300, blank=True, null=True)
    memory = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["model"]

    def __str__(self):
        return self.model
