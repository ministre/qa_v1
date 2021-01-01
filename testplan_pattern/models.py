from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TestplanPattern(models.Model):
    name = models.CharField(max_length=500)
    version = models.CharField(max_length=30)
    redmine_project = models.CharField(max_length=100, blank=True, null=True)
    redmine_project_name = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project_desc = models.CharField(max_length=1000, blank=True, null=True)
    redmine_parent = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='testplan_pattern_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='testplan_pattern_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name) + ' (' + str(self.version) + ')'


class CategoryPattern(models.Model):
    testplan_pattern = models.ForeignKey(TestplanPattern, related_name='testplan_pattern_category',
                                         on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    priority = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='pattern_category_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='pattern_category_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Pattern Categories"

    def __str__(self):
        return self.name
