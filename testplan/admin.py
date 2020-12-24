from django.contrib import admin
from testplan.models import TestPlan, Category, Test

admin.site.register(TestPlan)
admin.site.register(Category)
admin.site.register(Test)
