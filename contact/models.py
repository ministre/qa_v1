from django.db import models
from django.contrib.auth.models import User
from device.models import Vendor
from django.utils import timezone


class Contact(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, related_name='contact_vendor', on_delete=models.CASCADE, blank=True, null=True)
    username = models.ForeignKey(User, models.SET_NULL, related_name='contact_username', blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='contact_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='contact_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        order_with_respect_to = 'last_name'

    def __str__(self):
        full_name = str(self.last_name) + ' ' + str(self.first_name)
        if self.middle_name:
            full_name += ' ' + str(self.middle_name)
        return full_name
