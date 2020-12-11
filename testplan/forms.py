from django.forms import ModelForm
from testplan.models import Test, TestPlan
from django import forms


class TestPlanForm(ModelForm):
    class Meta:
        model = TestPlan
        labels = {
            'name': 'Программа и методика испытаний',
            'version': 'Редакция',
        }
        fields = ['name', 'version']


class TestForm(ModelForm):
    class Meta:
        model = Test
        labels = {
            'category': 'Категория',
            'name': 'Название теста',
            'url': 'URL Wiki-страницы в Redmine',
            'procedure': 'Процедура',
            'expected': 'Ожидаемый результат',
        }
        widgets = {'testplan': forms.HiddenInput()}
        fields = ['category', 'name', 'url', 'procedure', 'expected']
