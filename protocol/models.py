from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from device.models import Device
from testplan.models import TestPlan, Category, Test


class Protocol(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    testplan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    sw = models.CharField(max_length=50)
    sw_checksum = models.CharField(max_length=50, blank=True, null=True)
    engineer_login = models.CharField(max_length=50, blank=True, null=True)
    engineer_password = models.CharField(max_length=200, blank=True, null=True)
    sysinfo = models.TextField(blank=True, null=True)
    console = models.CharField(max_length=400, blank=True, null=True)
    date_of_start = models.DateField(default=datetime.now)
    date_of_finish = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='protocol_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='protocol_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    result = models.IntegerField(default=0)

    def __str__(self):
        name = 'ID: ' + str(self.id)
        if self.sw:
            name += ' / SW Ver.: ' + str(self.sw)
        if self.date_of_start:
            name += ' / Date of testing: ' + str(self.date_of_start.strftime('%d.%m.%Y'))
        if self.date_of_finish:
            name += ' - ' + str(self.date_of_finish.strftime('%d.%m.%Y'))
        return name

    def get_results(self, headers=False):
        results = []
        categories = Category.objects.filter(testplan=self.testplan).order_by('priority')
        for i, category in enumerate(categories):
            if headers:
                results.append({'header': True, 'num': i+1, 'category_name': category.name})
            tests = Test.objects.filter(cat=category).order_by('priority')
            for j, test in enumerate(tests):
                try:
                    result = TestResult.objects.get(protocol=self, test=test)
                    comment = result.comment
                    test_issues = TestResultIssue.objects.filter(result=result)
                    issues = []
                    for issue in test_issues:
                        issues.append(issue.text)
                    test_configs = TestResultConfig.objects.filter(result=result)
                    configs = []
                    for config in test_configs:
                        configs.append(config.id)
                    result_id = result.id
                    if result.redmine_wiki:
                        result_redmine_wiki = result.redmine_wiki
                    else:
                        result_redmine_wiki = None
                    result = result.result
                except TestResult.DoesNotExist:
                    result_id = result = comment = result_redmine_wiki = None
                    issues = configs = []
                results.append({'header': False,
                                'num': [i+1, j+1],
                                'category_name': test.cat,
                                'test_id': test.id,
                                'test_name': test.name,
                                'result_id': result_id,
                                'result_redmine_wiki': result_redmine_wiki,
                                'result': result,
                                'comment': comment,
                                'issues': issues,
                                'configs': configs})
        return results


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    comment = models.TextField(max_length=3000, blank=True)
    redmine_wiki = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    info = models.TextField(blank=True)
    config = models.TextField(blank=True)


class TestResultConfig(models.Model):
    result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='result_config')
    desc = models.CharField(max_length=1000, blank=True, null=True)
    lang = models.CharField(max_length=40, blank=True, null=True)
    config = models.TextField()
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_config_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_config_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class TestResultIssue(models.Model):
    result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='result_issue')
    text = models.TextField()
    ticket = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_issue_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_issue_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
