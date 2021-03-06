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
    general = forms.BooleanField(label=_('General Information'), required=False, initial=True)
    photos = forms.BooleanField(label=_('Photos'), required=False, initial=True)
    samples = forms.BooleanField(label=_('Samples'), required=False, initial=True)
    protocols = forms.BooleanField(label=_('Protocols'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(RedmineDeviceExportForm, self).__init__(*args, **kwargs)
        self.fields['device_id'].widget = forms.HiddenInput()


class RedmineTestExportForm(forms.Form):
    test_id = forms.IntegerField()
    redmine_project = forms.CharField(label=_('Project ID'), max_length=100)
    redmine_wiki = forms.CharField(label='Wiki', max_length=100)
    configs = forms.BooleanField(label=_('Configurations'), required=False, initial=True)
    images = forms.BooleanField(label=_('Images'), required=False, initial=True)
    files = forms.BooleanField(label=_('Files'), required=False, initial=True)
    links = forms.BooleanField(label=_('Links'), required=False, initial=True)
    comments = forms.BooleanField(label=_('Comments'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(RedmineTestExportForm, self).__init__(*args, **kwargs)
        self.fields['test_id'].widget = forms.HiddenInput()


class RedmineTestplanExportForm(forms.Form):
    testplan_id = forms.IntegerField()
    redmine_project = forms.CharField(label=_('Project ID'), max_length=100)
    redmine_project_name = forms.CharField(label=_('Project Name'), max_length=100)
    redmine_project_desc = forms.CharField(label=_('Project Description'), max_length=100)
    redmine_parent = forms.CharField(label=_('Parent Project ID'), max_length=100)
    test_list = forms.BooleanField(label=_('Test list'), required=False, initial=True)
    test_details_wiki = forms.BooleanField(label=_('Test details wiki'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(RedmineTestplanExportForm, self).__init__(*args, **kwargs)
        self.fields['testplan_id'].widget = forms.HiddenInput()


class RedmineResultExportForm(forms.Form):
    result_id = forms.IntegerField()
    redmine_project = forms.CharField(label=_('Project ID'), max_length=100)
    redmine_wiki = forms.CharField(label='Wiki', max_length=100)
    redmine_parent_wiki = forms.CharField(label=_('Parent Wiki'), max_length=100)
    test_desc = forms.BooleanField(label=_('Test Description'), required=False, initial=True)
    result_notes = forms.BooleanField(label=_('Notes'), required=False, initial=True)
    result_configs = forms.BooleanField(label=_('Configurations'), required=False, initial=True)
    result_images = forms.BooleanField(label=_('Images'), required=False, initial=True)
    result_files = forms.BooleanField(label=_('Files'), required=False, initial=True)
    result_summary = forms.BooleanField(label=_('Result'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(RedmineResultExportForm, self).__init__(*args, **kwargs)
        self.fields['result_id'].widget = forms.HiddenInput()


class RedmineProtocolExportForm(forms.Form):
    protocol_id = forms.IntegerField()
    redmine_project = forms.CharField(label=_('Project ID'), max_length=100)
    redmine_wiki = forms.CharField(label='Wiki', max_length=100)
    general = forms.BooleanField(label=_('Device information'), required=False, initial=True)
    results_list = forms.BooleanField(label=_('Test results list'), required=False, initial=True)
    results_wiki = forms.BooleanField(label=_('Test results wiki'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(RedmineProtocolExportForm, self).__init__(*args, **kwargs)
        self.fields['protocol_id'].widget = forms.HiddenInput()
