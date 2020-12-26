from django import forms
from django.utils.translation import gettext_lazy as _


class BuildDocxProtocolForm(forms.Form):
    protocol_id = forms.IntegerField()
    title_page = forms.BooleanField(label=_('Title Page'), required=False, initial=True)
    header = forms.BooleanField(label=_('Page Header'), required=False, initial=True)
    general = forms.BooleanField(label=_('Device Information'), required=False, initial=True)
    perfomance_table = forms.BooleanField(label=_('Perfomance Table'), required=False, initial=True)
    results_table = forms.BooleanField(label=_('Results Table'), required=False, initial=True)
    summary = forms.BooleanField(label=_('Summary'), required=False, initial=True)
    working_group = forms.BooleanField(label=_('Working Group'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(BuildDocxProtocolForm, self).__init__(*args, **kwargs)
        self.fields['protocol_id'].widget = forms.HiddenInput()
