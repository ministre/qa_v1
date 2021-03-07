from django.contrib import admin
from protocol.models import Protocol, TestResult, TestResultNote, TestResultConfig, TestResultImage, TestResultFile,\
    TestResultIssue, ProtocolFile, ProtocolAdditionalIssue

admin.site.register(Protocol)
admin.site.register(TestResult)
admin.site.register(TestResultNote)
admin.site.register(TestResultConfig)
admin.site.register(TestResultImage)
admin.site.register(TestResultFile)
admin.site.register(TestResultIssue)
admin.site.register(ProtocolFile)
admin.site.register(ProtocolAdditionalIssue)
