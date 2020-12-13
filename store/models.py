from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    date_of_received = models.DateField(default=timezone.now)
    date_of_returned = models.DateField(default=None, blank=True, null=True)
    received_by = models.ForeignKey(User, related_name='received_by_user', on_delete=models.CASCADE)
    returned_by = models.ForeignKey(User, related_name='returned_by_user', on_delete=models.CASCADE, blank=True,
                                    null=True)
