from django.forms import ModelForm
from docx_generator.models import DocxTemplateFile
from django.utils.translation import gettext_lazy as _
from django import forms


class DocxTemplateFileForm(ModelForm):
    class Meta:
        model = DocxTemplateFile
        labels = {
            'name': _('Name'),
            'type': _('Type'),
            'file': _('File'),
        }
        fields = '__all__'
        TEMPLATE_TYPE = (
            ('0', 'Protocol'),
            ('1', 'Detailed protocol'),
            ('2', 'Testplan'),
        )

        widgets = {
            'type': forms.Select(choices=TEMPLATE_TYPE, attrs={'class': 'form-control'}),
        }


class BuildProtocolForm(forms.Form):
    docx_template = forms.ModelChoiceField(queryset=DocxTemplateFile.objects.filter(type=0).order_by('-id'))


class BuildProtocolDetailedForm(forms.Form):
    docx_template = forms.ModelChoiceField(queryset=DocxTemplateFile.objects.filter(type=1).order_by('-id'))


class BuildTestplanForm(forms.Form):
    docx_template = forms.ModelChoiceField(queryset=DocxTemplateFile.objects.filter(type=2).order_by('-id'))
