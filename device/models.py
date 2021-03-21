from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
import os


class Vendor(models.Model):
    name = models.CharField(max_length=400)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='vendor_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='vendor_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def devices_count(self):
        count = Device.objects.filter(vendor=self).count()
        return count


class DeviceType(models.Model):
    name = models.CharField(max_length=300)
    redmine_project = models.CharField(max_length=100, blank=True, null=True)
    redmine_project_name = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project_desc = models.CharField(max_length=1000, blank=True, null=True)
    redmine_parent = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='device_type_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='device_type_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def devices_count(self):
        count = Device.objects.filter(type=self).count()
        return count


class Device(models.Model):
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    model = models.CharField(max_length=300)
    hw = models.CharField(max_length=50, blank=True, null=True)
    redmine_project = models.CharField(max_length=100, blank=True, null=True)
    redmine_project_name = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project_desc = models.CharField(max_length=1000, blank=True, null=True)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='device_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='device_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    #
    interfaces = models.CharField(max_length=300, blank=True, null=True)
    leds = models.CharField(max_length=300, blank=True, null=True)
    buttons = models.CharField(max_length=300, blank=True, null=True)
    chipsets = models.CharField(max_length=300, blank=True, null=True)
    memory = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["model"]

    def __str__(self):
        name = self.model
        if self.hw:
            name += ' (' + str(self.hw) + ')'
        return name

    def protocols_count(self):
        from protocol.models import Protocol
        count = Protocol.objects.filter(device=self).count()
        return count


class DevicePhoto(models.Model):
    device = models.ForeignKey(Device, related_name='device_photo', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="device/photos/")
    desc = models.CharField(max_length=1000)
    width = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    height = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='photo_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='photo_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.desc

    def filename(self):
        return os.path.basename(self.photo.name)


class DeviceSample(models.Model):
    device = models.ForeignKey(Device, related_name='device_sample', on_delete=models.CASCADE)
    sn = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='sample_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='sample_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sn


class DeviceSampleAccount(models.Model):
    sample = models.ForeignKey(DeviceSample, related_name='sample_account', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='sample_account_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='sample_account_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class DeviceFile(models.Model):
    device = models.ForeignKey(Device, related_name='device_file', on_delete=models.CASCADE)
    type = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to="device/files/")
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='file_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='file_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def filename(self):
        return os.path.basename(self.file.name)


class DeviceNote(models.Model):
    device = models.ForeignKey(Device, related_name='device_note', on_delete=models.CASCADE)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    text = models.TextField()
    format = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='note_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='note_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class DeviceContact(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    contact = models.ForeignKey('contact.Contact', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='d_contact_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='d_contact_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
