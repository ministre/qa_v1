from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class DocxProfile(models.Model):
    name = models.CharField(max_length=1000)
    header_logo = models.FileField(upload_to="docx_builder/files/", blank=True, null=True)
    header_text1 = models.CharField(max_length=1000, blank=True, null=True)
    header_text2 = models.CharField(max_length=1000, blank=True, null=True)
    title_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    title_font_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    title_font_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    title_font_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    title_font_size = models.IntegerField(default=20, validators=[MinValueValidator(10), MaxValueValidator(40)])
    title_font_bold = models.BooleanField(blank=True, null=True, default=True)
    title_font_italic = models.BooleanField(blank=True, null=True, default=False)
    title_font_underline = models.BooleanField(blank=True, null=True, default=False)
    title_space_before = models.IntegerField(default=12, validators=[MinValueValidator(0), MaxValueValidator(40)])
    title_space_after = models.IntegerField(default=12, validators=[MinValueValidator(0), MaxValueValidator(40)])
    title_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    h1_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    h1_font_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h1_font_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h1_font_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h1_font_size = models.IntegerField(default=16, validators=[MinValueValidator(10), MaxValueValidator(40)])
    h1_font_bold = models.BooleanField(blank=True, null=True, default=True)
    h1_font_italic = models.BooleanField(blank=True, null=True, default=False)
    h1_font_underline = models.BooleanField(blank=True, null=True, default=False)
    h1_space_before = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h1_space_after = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h1_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    h2_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    h2_font_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h2_font_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h2_font_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h2_font_size = models.IntegerField(default=14, validators=[MinValueValidator(10), MaxValueValidator(40)])
    h2_font_bold = models.BooleanField(blank=True, null=True, default=True)
    h2_font_italic = models.BooleanField(blank=True, null=True, default=False)
    h2_font_underline = models.BooleanField(blank=True, null=True, default=False)
    h2_space_before = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h2_space_after = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h2_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    created_by = models.ForeignKey(User, models.SET_NULL, related_name='docx_profile_c', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, models.SET_NULL, related_name='docx_profile_u', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
