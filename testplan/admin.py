from django.contrib import admin
from testplan.models import TestPlan, Category, Test, TestConfig

admin.site.register(TestPlan)
admin.site.register(Category)
admin.site.register(Test)
admin.site.register(TestConfig)
