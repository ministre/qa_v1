from django.contrib import admin
from testplan.models import TestPlan, Category, Test, TestConfig, TestImage, TestFile, TestLink, TestComment

admin.site.register(TestPlan)
admin.site.register(Category)
admin.site.register(Test)
admin.site.register(TestConfig)
admin.site.register(TestImage)
admin.site.register(TestFile)
admin.site.register(TestLink)
admin.site.register(TestComment)
