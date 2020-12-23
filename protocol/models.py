from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from device.models import Device
from testplan.models import TestPlan, Test


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

    def get_results(self):
        results = TestResult.objects.filter(protocol=self).order_by('id')
        tests = []
        category = None
        i = j = 0
        for result in results:
            new_category = result.test.category
            if new_category == category:
                j = j + 1
                result_issues = []
                issues = TestResultIssue.objects.filter(result=result).order_by('id')
                for issue in issues:
                    result_issues.append({'id': issue.id, 'text': issue.text, 'ticket': issue.ticket})
                result_configs = []
                configs = TestResultConfig.objects.filter(result=result).order_by('id')
                for config in configs:
                    result_configs.append(config.id)
                tests.append({'test_id': result.test.id,
                              'test_num': str(i) + '.' + str(j),
                              'test_name': result.test.name,
                              'test_category': result.test.category,
                              'result_id': result.id,
                              'result_result': result.result,
                              'result_comment': result.comment,
                              'result_issues': result_issues,
                              'result_configs': result_configs
                              })
            else:
                i = i + 1
                j = 1
                result_issues = []
                issues = TestResultIssue.objects.filter(result=result).order_by('id')
                for issue in issues:
                    result_issues.append({'id': issue.id, 'text': issue.text, 'ticket': issue.ticket})
                result_configs = []
                configs = TestResultConfig.objects.filter(result=result).order_by('id')
                for config in configs:
                    result_configs.append(config.id)
                tests.append({'test_id': result.test.id,
                              'test_num': str(i) + '.' + str(j),
                              'test_name': result.test.name,
                              'test_category': result.test.category,
                              'result_id': result.id,
                              'result_result': result.result,
                              'result_comment': result.comment,
                              'result_issues': result_issues,
                              'result_configs': result_configs
                              })
                category = result.test.category
        return tests


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    info = models.TextField(default=None, blank=True, null=True)
    config = models.TextField(default=None, blank=True, null=True)


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
