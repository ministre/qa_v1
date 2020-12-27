from django.forms import ModelForm, HiddenInput
from .models import TechReq, TechReqFile
from django.utils.translation import gettext_lazy as _


class TechReqForm(ModelForm):
    class Meta:
        model = TechReq
        labels = {
            'device_type': _('Device Type'),
            'name': _('Document Name'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class TechReqFileForm(ModelForm):
    class Meta:
        model = TechReqFile
        labels = {
            'file': _('File'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'tech_req': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
