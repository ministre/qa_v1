from django import forms
from django.utils.translation import gettext_lazy as _


class RedmineDeviceTypeExportForm(forms.Form):
    device_type_id = forms.IntegerField()
    redmine_project = forms.CharField(label=_('Project ID'), max_length=100)
    redmine_project_name = forms.CharField(label=_('Project Name'), max_length=1000)
    redmine_project_desc = forms.CharField(label=_('Project Description'), max_length=100, required=False)
    redmine_parent = forms.CharField(label=_('Parent Project'), max_length=100, required=False)
    general_info = forms.BooleanField(label=_('General Information'), required=False)

    def __init__(self, *args, **kwargs):
        super(RedmineDeviceTypeExportForm, self).__init__(*args, **kwargs)
        self.fields['device_type_id'].widget = forms.HiddenInput()


class RedmineDeviceExportForm(forms.Form):
    device_id = forms.IntegerField()
    redmine_project = forms.CharField(label=_('Project ID'), max_length=100)
    redmine_project_name = forms.CharField(label=_('Project Name'), max_length=1000)
    redmine_project_desc = forms.CharField(label=_('Project Description'), max_length=100, required=False)
    redmine_parent = forms.CharField(label=_('Parent Project'), max_length=100, required=False)
    general_info = forms.BooleanField(label=_('General Information'), required=False)
    protocols = forms.BooleanField(label=_('Protocol List'), required=False)

    def __init__(self, *args, **kwargs):
        super(RedmineDeviceExportForm, self).__init__(*args, **kwargs)
        self.fields['device_id'].widget = forms.HiddenInput()


class RedmineProtocolExportForm(forms.Form):
    protocol_id = forms.IntegerField()
    redmine_project = forms.CharField(label=_('Project ID'), max_length=100)
    redmine_wiki = forms.CharField(label=_('Project Wiki'), max_length=100)
    general = forms.BooleanField(label=_('General Information'), required=False)
    results = forms.BooleanField(label=_('Test Results'), required=False)

    def __init__(self, *args, **kwargs):
        super(RedmineProtocolExportForm, self).__init__(*args, **kwargs)
        self.fields['protocol_id'].widget = forms.HiddenInput()
