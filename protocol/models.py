from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from device.models import Device
from testplan.models import TestPlan, Category, Test
from django.core.validators import MinValueValidator
import os


class Protocol(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    testplan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    sw = models.CharField(max_length=50)
    sw_checksum = models.CharField(max_length=50, blank=True, null=True)
    engineer_login = models.CharField(max_length=50, blank=True, null=True)
    engineer_password = models.CharField(max_length=200, blank=True, null=True)
    sysinfo = models.TextField(blank=True)
    console = models.CharField(max_length=400, blank=True, null=True)
    date_of_start = models.DateField(default=datetime.now)
    date_of_finish = models.DateField(blank=True, null=True)
    redmine_wiki = models.CharField(max_length=100, blank=True, null=True)
    result = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='protocol_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='protocol_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

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

                    # notes
                    test_notes = TestResultNote.objects.filter(result=result).order_by('id')
                    notes = []
                    for note in test_notes:
                        notes.append({'id': note.id, 'desc': note.desc, 'format': note.format, 'text': note.text})
                    # configs
                    test_configs = TestResultConfig.objects.filter(result=result).order_by('id')
                    configs = []
                    for config in test_configs:
                        configs.append({'id': config.id, 'desc': config.desc, 'config': config.config})
                    # images
                    test_images = TestResultImage.objects.filter(result=result).order_by('id')
                    images = []
                    for image in test_images:
                        images.append({'id': image.id})
                    # files
                    test_files = TestResultFile.objects.filter(result=result).order_by('id')
                    files = []
                    for file in test_files:
                        files.append({'id': file.id})
                    # issues
                    test_issues = TestResultIssue.objects.filter(result=result).order_by('id')
                    issues = []
                    for issue in test_issues:
                        issues.append(issue.text)

                    result_id = result.id
                    if result.redmine_wiki:
                        result_redmine_wiki = result.redmine_wiki
                    else:
                        result_redmine_wiki = None
                    result = result.result
                except TestResult.DoesNotExist:
                    result_id = result = comment = result_redmine_wiki = None
                    notes = configs = images = files = issues = []
                results.append({'header': False,
                                'num': [i+1, j+1],
                                'category_name': test.cat,
                                'test_id': test.id,
                                'test_name': test.name,
                                'test_purpose': test.purpose,
                                'test_procedure': test.procedure,
                                'test_expected': test.expected,
                                'result_id': result_id,
                                'result_redmine_wiki': result_redmine_wiki,
                                'result': result,
                                'comment': comment,
                                'notes': notes,
                                'configs': configs,
                                'images': images,
                                'files': files,
                                'issues': issues})
        return results

    def get_issues(self):
        issues = []
        categories = Category.objects.filter(testplan=self.testplan).order_by('priority')
        for category in categories:
            tests = Test.objects.filter(cat=category).order_by('priority')
            for test in tests:
                try:
                    result = TestResult.objects.get(protocol=self, test=test)
                    test_issues = TestResultIssue.objects.filter(result=result).order_by('id')
                    for issue in test_issues:
                        issues.append({'issue_id': issue.id, 'result_id': result.id, 'test_id': test.id,
                                       'text': issue.text})
                except TestResult.DoesNotExist:
                    pass
        return issues


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    comment = models.TextField(max_length=3000, blank=True)
    redmine_wiki = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class TestResultNote(models.Model):
    result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='result_note')
    desc = models.CharField(max_length=1000, blank=True, null=True)
    text = models.TextField()
    format = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_note_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_note_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class TestResultConfig(models.Model):
    result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='result_config')
    desc = models.CharField(max_length=1000, blank=True, null=True)
    lang = models.CharField(max_length=40, blank=True, null=True)
    config = models.TextField()
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_config_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_config_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class TestResultImage(models.Model):
    result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='result_image')
    desc = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to="protocol/results/images/")
    width = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    height = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_image_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_image_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class TestResultFile(models.Model):
    result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='result_file')
    desc = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to="protocol/results/files/")
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_file_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_file_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def filename(self):
        return os.path.basename(self.file.name)


class TestResultIssue(models.Model):
    result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='result_issue')
    text = models.TextField()
    ticket = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='result_issue_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='result_issue_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)


class ProtocolFile(models.Model):
    protocol = models.ForeignKey(Protocol, related_name='protocol_file', on_delete=models.CASCADE)
    type = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to="protocol/files/")
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='protocol_file_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='protocol_file_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def filename(self):
        return os.path.basename(self.file.name)
