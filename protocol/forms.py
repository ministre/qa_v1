from django.forms import ModelForm, HiddenInput
from protocol.models import Protocol, TestResult
from django.utils.translation import gettext_lazy as _
from django import forms


class ProtocolForm(ModelForm):
    class Meta:
        model = Protocol
        labels = {
            'device': _('Device'),
            'testplan': _('Testplan'),
            'sw': _('Software Version'),
            'sw_checksum': _('Checksum'),
            'engineer_login': _('Engineer Login'),
            'engineer_password': _('Engineer Password'),
            'sysinfo': _('System Information'),
            'console': _('Console port parameters'),
            'date_of_start': _('Started'),
            'date_of_finish': _('Completed'),
        }
        fields = '__all__'


class TestResultForm(ModelForm):
    class Meta:
        model = TestResult
        labels = {
            'result': _('Result'),
            'config': _('Configuration'),
            'info': _('Additional Information'),
            'comment': _('Comments'),
        }
        fields = '__all__'
        STATUS = (
            ('0', 'Не тестировался'),
            ('1', 'Не пройден'),
            ('2', 'Пройден с замечаниями'),
            ('3', 'Пройден'),
        )

        widgets = {
            'result': forms.Select(choices=STATUS, attrs={'class': 'form-control'}),
            'test': HiddenInput(), 'protocol': HiddenInput(),
        }
