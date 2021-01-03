from django.contrib import admin
from protocol.models import Protocol, TestResult, TestResultNote, TestResultConfig, TestResultImage, TestResultIssue

admin.site.register(Protocol)
admin.site.register(TestResult)
admin.site.register(TestResultNote)
admin.site.register(TestResultConfig)
admin.site.register(TestResultImage)
admin.site.register(TestResultIssue)
