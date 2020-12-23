from django.contrib import admin
from protocol.models import Protocol, TestResult, TestResultConfig, TestResultIssue

# Register your models here.

admin.site.register(Protocol)
admin.site.register(TestResult)
admin.site.register(TestResultConfig)
admin.site.register(TestResultIssue)
