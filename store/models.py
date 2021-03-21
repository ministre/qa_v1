from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    date_of_received = models.DateTimeField(default=timezone.now)
    date_of_returned = models.DateTimeField(default=None, blank=True, null=True)
    received_by = models.ForeignKey(User, models.SET_NULL, related_name='received_by_user', blank=True, null=True)
    returned_by = models.ForeignKey(User, models.SET_NULL, related_name='returned_by_user', blank=True, null=True)
