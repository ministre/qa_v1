from django.db import models


class DocxTemplateFile(models.Model):
    name = models.CharField(max_length=300)
    type = models.IntegerField(default=0)
    file = models.FileField(upload_to='docx_generator/docx_templates/')

    def __str__(self):
        return self.name
