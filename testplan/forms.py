from django.forms import ModelForm, HiddenInput
from .models import TestPlan, Category, Test
from django.utils.translation import gettext_lazy as _


class TestPlanForm(ModelForm):
    class Meta:
        model = TestPlan
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
        super(TestPlanForm, self).__init__(*args, **kwargs)
        self.fields['redmine_parent'].initial = 'testplans'


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        labels = {
            'name': _('Name'),
            'redmine_project': _('Redmine Project'),
            'redmine_project_name': _('Redmine Project Name'),
            'redmine_project_desc': _('Redmine Project Description'),
            'redmine_parent': _('Redmine Parent Project'),
        }
        fields = '__all__'
        widgets = {'testplan': HiddenInput(), 'priority': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class TestForm(ModelForm):
    class Meta:
        model = Test
        labels = {
            'name': _('Name'),
            'purpose': _('Purpose'),
            'procedure': _('Procedure'),
            'expected': _('Expected result'),
            'redmine_wiki': 'Redmine Wiki',
        }
        fields = '__all__'
        widgets = {'cat': HiddenInput(), 'priority': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}
