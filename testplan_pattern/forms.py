from django.forms import ModelForm, HiddenInput
from .models import TestplanPattern, CategoryPattern, TestPattern
from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404


class TestplanPatternForm(ModelForm):
    class Meta:
        model = TestplanPattern
        labels = {
            'name': _('Name'),
            'version': _('Version'),
            'redmine_project': _('Redmine Project'),
            'redmine_project_name': _('Redmine Project Name'),
            'redmine_project_desc': _('Redmine Project Description'),
            'redmine_parent': _('Redmine Parent Project'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(TestplanPatternForm, self).__init__(*args, **kwargs)
        self.fields['redmine_parent'].initial = 'testplan_patterns'


class CategoryPatternForm(ModelForm):
    class Meta:
        model = CategoryPattern
        labels = {
            'name': _('Name'),
            'redmine_project': _('Redmine Project'),
            'redmine_project_name': _('Redmine Project Name'),
            'redmine_project_desc': _('Redmine Project Description'),
            'redmine_parent': _('Redmine Parent Project'),
        }
        fields = '__all__'
        widgets = {'testplan_pattern': HiddenInput(), 'priority': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class TestPatternForm(ModelForm):
    class Meta:
        model = TestPattern
        labels = {
            'name': _('Name'),
            'purpose': _('Purpose'),
            'procedure': _('Procedure'),
            'expected': _('Expected result'),
            'redmine_wiki': 'Redmine Wiki',
        }
        fields = '__all__'
        widgets = {'category_pattern': HiddenInput(),
                   'priority': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class TestNamesUpdateForm(forms.Form):
    pattern_id = forms.IntegerField()
    name = forms.CharField(label=_('Name'), max_length=300)
    tests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label=_('Dependencies'), required=False)

    def __init__(self, *args, **kwargs):
        pattern_id = kwargs.pop('pattern_id', None)
        super(TestNamesUpdateForm, self).__init__(*args, **kwargs)
        self.fields['pattern_id'].initial = pattern_id
        self.fields['pattern_id'].widget = forms.HiddenInput()
        test_pattern = get_object_or_404(TestPattern, id=pattern_id)
        subs = test_pattern.get_subs()
        self.fields['tests'].choices = subs
        self.fields['tests'].initial = [item[0] for item in subs]


class TestPurposesUpdateForm(forms.Form):
    pattern_id = forms.IntegerField()
    purpose = forms.CharField(label=_('Purpose'), max_length=1000)
    tests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label=_('Dependencies'), required=False)

    def __init__(self, *args, **kwargs):
        pattern_id = kwargs.pop('pattern_id', None)
        super(TestPurposesUpdateForm, self).__init__(*args, **kwargs)
        self.fields['pattern_id'].initial = pattern_id
        self.fields['pattern_id'].widget = forms.HiddenInput()
        test_pattern = get_object_or_404(TestPattern, id=pattern_id)
        subs = test_pattern.get_subs()
        self.fields['tests'].choices = subs
        self.fields['tests'].initial = [item[0] for item in subs]


class TestProceduresUpdateForm(forms.Form):
    pattern_id = forms.IntegerField()
    procedure = forms.CharField(widget=forms.Textarea, label=_('Procedure'))
    tests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label=_('Dependencies'), required=False)

    def __init__(self, *args, **kwargs):
        pattern_id = kwargs.pop('pattern_id', None)
        super(TestProceduresUpdateForm, self).__init__(*args, **kwargs)
        self.fields['pattern_id'].initial = pattern_id
        self.fields['pattern_id'].widget = forms.HiddenInput()
        test_pattern = get_object_or_404(TestPattern, id=pattern_id)
        subs = test_pattern.get_subs()
        self.fields['tests'].choices = subs
        self.fields['tests'].initial = [item[0] for item in subs]


class TestExpectedUpdateForm(forms.Form):
    pattern_id = forms.IntegerField()
    expected = forms.CharField(widget=forms.Textarea, label=_('Expected result'))
    tests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label=_('Dependencies'), required=False)

    def __init__(self, *args, **kwargs):
        pattern_id = kwargs.pop('pattern_id', None)
        super(TestExpectedUpdateForm, self).__init__(*args, **kwargs)
        self.fields['pattern_id'].initial = pattern_id
        self.fields['pattern_id'].widget = forms.HiddenInput()
        test_pattern = get_object_or_404(TestPattern, id=pattern_id)
        subs = test_pattern.get_subs()
        self.fields['tests'].choices = subs
        self.fields['tests'].initial = [item[0] for item in subs]


class TestRedmineWikiUpdateForm(forms.Form):
    pattern_id = forms.IntegerField()
    redmine_wiki = forms.CharField(max_length=300)
    tests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label=_('Dependencies'), required=False)

    def __init__(self, *args, **kwargs):
        pattern_id = kwargs.pop('pattern_id', None)
        super(TestRedmineWikiUpdateForm, self).__init__(*args, **kwargs)
        self.fields['pattern_id'].initial = pattern_id
        self.fields['pattern_id'].widget = forms.HiddenInput()
        test_pattern = get_object_or_404(TestPattern, id=pattern_id)
        subs = test_pattern.get_subs()
        self.fields['tests'].choices = subs
        self.fields['tests'].initial = [item[0] for item in subs]
