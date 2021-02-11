from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from testplan_pattern.models import TestplanPattern, CategoryPattern, TestPattern, TestPatternConfig, TestPatternImage


class TestPlan(models.Model):
    name = models.CharField(max_length=500)
    version = models.CharField(max_length=30)
    redmine_project = models.CharField(max_length=100, blank=True, null=True)
    redmine_project_name = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project_desc = models.CharField(max_length=1000, blank=True, null=True)
    redmine_parent = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey(TestplanPattern, models.SET_NULL, related_name='parent_testplan', blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='testplan_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='testplan_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Testplans"

    def __str__(self):
        return str(self.name) + ' (' + str(self.version) + ')'

    def tests_count(self):
        i = 0
        categories = Category.objects.filter(testplan=self)
        for category in categories:
            tests = Test.objects.filter(cat=category)
            for _ in tests:
                i += 1
        return i

    def get_protocols(self):
        from protocol.models import Protocol
        testplan_protocols = []
        protocols = Protocol.objects.filter(testplan=self).order_by('id')
        for protocol in protocols:
            testplan_protocols.append({'id': protocol.id, 'device': protocol.device, 'firmware': protocol.sw})
        return testplan_protocols


class Category(models.Model):
    testplan = models.ForeignKey(TestPlan, related_name='testplan_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    priority = models.IntegerField(default=0)
    parent = models.ForeignKey(CategoryPattern, models.SET_NULL, related_name='parent_category', blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='category_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='category_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Test(models.Model):
    cat = models.ForeignKey(Category, related_name='cat_test', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    purpose = models.CharField(max_length=1000, null=True, blank=True)
    procedure = models.TextField(blank=True)
    expected = models.TextField(blank=True)
    priority = models.IntegerField(default=0)
    parent = models.ForeignKey(TestPattern, models.SET_NULL, related_name='parent_test', blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='test_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='test_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    redmine_wiki = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_num(self):
        categories = Category.objects.filter(testplan=self.cat.testplan).order_by('priority')
        for i, category in enumerate(categories):
            tests = Test.objects.filter(cat=category).order_by('priority')
            for j, test in enumerate(tests):
                if test == self:
                    return [i+1, j+1]
        return []


class TestConfig(models.Model):
    test = models.ForeignKey(Test, related_name='test_config', on_delete=models.CASCADE)
    parent = models.ForeignKey(TestPatternConfig, related_name='parent_config', on_delete=models.CASCADE,
                               blank=True, null=True)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    lang = models.CharField(max_length=40, blank=True, null=True)
    config = models.TextField(blank=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='test_config_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='test_config_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class TestImage(models.Model):
    test = models.ForeignKey(Test, related_name='test_image', on_delete=models.CASCADE)
    parent = models.ForeignKey(TestPatternImage, related_name='parent_image', on_delete=models.CASCADE,
                               blank=True, null=True)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to="testplan/images/", blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='test_image_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='test_image_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
