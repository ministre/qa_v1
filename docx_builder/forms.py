from django import forms
from django.utils.translation import gettext_lazy as _


class BuildDocxProtocolForm(forms.Form):
    protocol_id = forms.IntegerField()
    title_page = forms.BooleanField(label=_('Title page'), required=False, initial=True)
    header = forms.BooleanField(label=_('Page header'), required=False, initial=True)
    general = forms.BooleanField(label=_('Device information'), required=False, initial=True)
    performance = forms.BooleanField(label=_('Performance results'), required=False, initial=True)
    results_table = forms.BooleanField(label=_('Test results'), required=False, initial=True)
    summary = forms.BooleanField(label=_('Summary'), required=False, initial=True)
    team = forms.BooleanField(label=_('Testing team'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(BuildDocxProtocolForm, self).__init__(*args, **kwargs)
        self.fields['protocol_id'].widget = forms.HiddenInput()
