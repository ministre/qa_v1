from django.forms import ModelForm, HiddenInput
from protocol.models import Protocol, TestResult, TestResultConfig
from django.utils.translation import gettext_lazy as _
from django import forms
from django.db.models import Q


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
            'result': _('Result'),
        }
        fields = '__all__'
        RESULT = (
            ('0', _('Testing')),
            ('1', _('Not recommended')),
            ('2', _('Limited')),
            ('3', _('Recommended')),
        )
        widgets = {
            'result': forms.Select(choices=RESULT, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ResultForm(ModelForm):
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


class ProtocolCopyResultsForm(forms.Form):
    src_protocol = forms.ModelChoiceField(queryset=Protocol.objects.all(), label=_('Source Protocol'))
    dst_protocol = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        device_id = kwargs.pop('device_id', None)
        dst_protocol = kwargs.pop('dst_protocol', None)
        super(ProtocolCopyResultsForm, self).__init__(*args, **kwargs)

        self.fields['dst_protocol'].initial = dst_protocol
        self.fields['dst_protocol'].widget = forms.HiddenInput()
        if device_id:
            self.fields['src_protocol'].queryset = Protocol.objects.filter(Q(device=device_id) & ~Q(id=dst_protocol))


class ResultConfigForm(ModelForm):
    class Meta:
        model = TestResultConfig
        labels = {
            'desc': _('Description'),
            'lang': _('Style'),
            'config': _('Configuration'),
        }
        fields = '__all__'
        LANG = (
            ('json', 'JSON'),
            ('c', 'C'),
            ('coffee', 'Coffeescript'),
            ('csharp', 'C#'),
            ('css', 'CSS'),
            ('d', 'D'),
            ('go', 'Go'),
            ('haskell', 'Haskell'),
            ('html', 'HTML'),
            ('javascript', 'JavaScript'),
            ('lua', 'Lua'),
            ('php', 'PHP'),
            ('python', 'Python'),
            ('r', 'R'),
            ('ruby', 'Ruby'),
            ('scheme', 'Scheme'),
            ('shell', 'Shell'),
        )
        widgets = {
            'result': HiddenInput(),
            'lang': forms.Select(choices=LANG, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
