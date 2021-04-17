from django.contrib import admin
from .models import TestplanPattern, CategoryPattern, TestPattern, TestPatternConfig, TestPatternImage, \
    TestPatternFile, TestPatternLink, TestPatternComment, TestPatternValueInteger, TestPatternValueIntegerPair, \
    TestPatternValueText

admin.site.register(TestplanPattern)
admin.site.register(CategoryPattern)
admin.site.register(TestPattern)
admin.site.register(TestPatternConfig)
admin.site.register(TestPatternImage)
admin.site.register(TestPatternFile)
admin.site.register(TestPatternLink)
admin.site.register(TestPatternComment)
admin.site.register(TestPatternValueInteger)
admin.site.register(TestPatternValueIntegerPair)
admin.site.register(TestPatternValueText)
