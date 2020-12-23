from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TestPlan(models.Model):
    name = models.CharField(max_length=500)
    version = models.CharField(max_length=30)
    redmine_project = models.CharField(max_length=100, blank=True, null=True)
    redmine_project_name = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project_desc = models.CharField(max_length=1000, blank=True, null=True)
    redmine_parent = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='testplan_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='testplan_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name) + ' (' + str(self.version) + ')'

    def protocols_count(self):
        from protocol.models import Protocol
        count = Protocol.objects.filter(testplan=self).count()
        return count


class Category(models.Model):
    testplan = models.ForeignKey(TestPlan, related_name='testplan_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    priority = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='category_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='category_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Test(models.Model):
    cat = models.ForeignKey(Category, related_name='cat_test', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=300)
    purpose = models.TextField(max_length=5000, null=True, blank=True)
    procedure = models.TextField()
    expected = models.TextField()
    priority = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='test_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='test_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    #
    url = models.CharField(max_length=300, null=True, blank=True)
    testplan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    category = models.CharField(max_length=300)

    def __str__(self):
        return self.name
