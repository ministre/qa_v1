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
            ('0', _('Protocol')),
            ('1', _('Detailed protocol')),
            ('2', _('Testplan')),
        )

        widgets = {
            'type': forms.Select(choices=TEMPLATE_TYPE, attrs={'class': 'form-control'}),
        }


class BuildProtocolForm(forms.Form):
    protocol_id = forms.IntegerField()
    docx_template_id = forms.ModelChoiceField(queryset=DocxTemplateFile.objects.filter(type=0).order_by('-id'),
                                              label=_('Template'))


class BuildProtocolDetailedForm(forms.Form):
    protocol_id = forms.IntegerField()
    docx_template_id = forms.ModelChoiceField(queryset=DocxTemplateFile.objects.filter(type=1).order_by('-id'),
                                              label=_('Template'))


class BuildTestplanForm(forms.Form):
    testplan_id = forms.IntegerField()
    docx_template_id = forms.ModelChoiceField(queryset=DocxTemplateFile.objects.filter(type=2).order_by('-id'),
                                              label=_('Template'))
