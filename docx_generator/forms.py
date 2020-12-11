from django.forms import ModelForm
from docx_generator.models import DocxTemplateFile


class DocxTemplateForm(ModelForm):
    class Meta:
        model = DocxTemplateFile
        labels = {
            'title': 'Имя шаблона',
            'upload': 'Загрузка файла',
        }
        fields = ['title', 'upload']
