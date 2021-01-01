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

    def tests_count(self):
        i = 0
        categories = CategoryPattern.objects.filter(testplan_pattern=self)
        for category in categories:
            tests = TestPattern.objects.filter(category_pattern=category)
            for _ in tests:
                i += 1
        return i


class CategoryPattern(models.Model):
    testplan_pattern = models.ForeignKey(TestplanPattern, related_name='testplan_pattern_category',
                                         on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    priority = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='category_pattern_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='category_pattern_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Pattern Categories"

    def __str__(self):
        return self.name


class TestPattern(models.Model):
    category_pattern = models.ForeignKey(CategoryPattern, related_name='category_pattern_test',
                                         on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    purpose = models.CharField(max_length=1000, null=True, blank=True)
    procedure = models.TextField(blank=True)
    expected = models.TextField(blank=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='test_pattern_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='test_pattern_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    redmine_wiki = models.CharField(max_length=300, null=True, blank=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_num(self):
        categories = \
            CategoryPattern.objects.filter(testplan_pattern=self.category_pattern.testplan_pattern).order_by('priority')
        for i, category in enumerate(categories):
            tests = TestPattern.objects.filter(category_pattern=category).order_by('priority')
            for j, test in enumerate(tests):
                if test == self:
                    return [i+1, j+1]
        return []
