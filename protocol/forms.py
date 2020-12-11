from django import forms
from django.forms import ModelForm
from protocol.models import Protocol


class ProtocolForm(ModelForm):
    class Meta:
        model = Protocol
        labels = {
            'sw': 'ПО',
            'sw_checksum': 'Контрольная сумма ПО',
            'engineer_login': 'Заводской (инженерный) логин',
            'engineer_password': 'Заводской (инженерный) пароль',
            'sysinfo': 'Системная информация',
            'console': 'Параметры консольного порта',
            'date_of_start': 'Дата начала тестирования',
            'date_of_finish': 'Дата окончания тестирования',
        }
        fields = ['sw', 'sw_checksum',
                  'engineer_login', 'engineer_password', 'sysinfo', 'console',
                  'date_of_start', 'date_of_finish']

    def __init__(self, *args, **kwargs):
        super(ProtocolForm, self).__init__(*args, **kwargs)
        self.fields['sw_checksum'].required = False
        self.fields['engineer_login'].required = False
        self.fields['engineer_password'].required = False
        self.fields['sysinfo'].required = False
        self.fields['console'].required = False


class ResultsForm(forms.Form):
    config = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': "15", }))
    info = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': "15", }))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': "15", }))
