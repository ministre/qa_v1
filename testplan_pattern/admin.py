from django.contrib import admin
from .models import TestplanPattern, CategoryPattern, TestPattern

admin.site.register(TestplanPattern)
admin.site.register(CategoryPattern)
admin.site.register(TestPattern)
