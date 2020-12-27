from django.forms import ModelForm, HiddenInput
from .models import TechReq
from django.utils.translation import gettext_lazy as _


class TechReqForm(ModelForm):
    class Meta:
        model = TechReq
        labels = {
            'type': _('Device Type'),
            'name': _('Document Name'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
