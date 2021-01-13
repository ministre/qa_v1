from django.forms import ModelForm, HiddenInput
from .models import TestplanPattern, CategoryPattern, TestPattern
from django import forms
from django.utils.translation import gettext_lazy as _


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


class TestsUpdateForm(forms.Form):
    CHOICES = [
        ("a", "A"),
        ("b", "B"),
    ]
    name = forms.CharField(label=_('Name'), max_length=100)
    picked_tests = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple(), initial=('b'))
