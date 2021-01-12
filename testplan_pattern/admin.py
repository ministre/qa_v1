from django.contrib import admin
from .models import TestplanPattern, CategoryPattern, TestPattern, TestImagePattern, TestConfigPattern, \
    TestLinkPattern, TestCommentPattern

admin.site.register(TestplanPattern)
admin.site.register(CategoryPattern)
admin.site.register(TestPattern)
admin.site.register(TestImagePattern)
admin.site.register(TestConfigPattern)
admin.site.register(TestLinkPattern)
admin.site.register(TestCommentPattern)
