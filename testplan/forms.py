from django.forms import ModelForm
from testplan.models import Test, TestPlan
from django import forms
from django.utils.translation import gettext_lazy as _


class TestPlanForm(ModelForm):
    class Meta:
        model = TestPlan
        labels = {
            'name': _('Name'),
            'version': _('Version'),
        }
        fields = '__all__'


class TestForm(ModelForm):
    class Meta:
        model = Test
        labels = {
            'category': _('Category'),
            'name': _('Name'),
            'url': _('Redmine Wiki page'),
            'procedure': _('Procedure'),
            'expected': _('Expected result'),
        }
        widgets = {'testplan': forms.HiddenInput()}
        fields = '__all__'
