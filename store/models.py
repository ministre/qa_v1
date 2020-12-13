from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Item(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    comment = models.CharField(max_length=500)
    date_of_received = models.DateField(default=datetime.now, blank=True)
    date_of_returned = models.DateField(default=None, blank=True, null=True)
    received_by = models.ForeignKey(User, related_name='received_by_user', on_delete=models.CASCADE, blank=True)
    returned_by = models.ForeignKey(User, related_name='returned_by_user', on_delete=models.CASCADE, blank=True,
                                    null=True)
