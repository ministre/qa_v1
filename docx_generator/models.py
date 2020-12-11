from django.db import models


class DocxTemplateFile(models.Model):
    title = models.CharField(max_length=300)
    upload = models.FileField(upload_to='docx_templates/')
