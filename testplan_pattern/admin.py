from django.contrib import admin
from .models import TestplanPattern, CategoryPattern, TestPattern, TestPatternConfig, TestPatternImage, \
    TestPatternFile, TestPatternLink, TestPatternComment

admin.site.register(TestplanPattern)
admin.site.register(CategoryPattern)
admin.site.register(TestPattern)
admin.site.register(TestPatternConfig)
admin.site.register(TestPatternImage)
admin.site.register(TestPatternFile)
admin.site.register(TestPatternLink)
admin.site.register(TestPatternComment)
