from django.forms import ModelForm, HiddenInput
from protocol.models import Protocol, TestResult, TestResultNote, TestResultConfig, TestResultImage, TestResultFile,\
    TestResultIssue, ProtocolFile, ProtocolAdditionalIssue
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
            'result': _('Result'),
            'date_of_start': _('Started'),
            'date_of_finish': _('Completed'),
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
            'comment': _('Comment'),
            'redmine_wiki': 'Redmine Wiki',
        }
        fields = '__all__'
        STATUS = (
            ('0', _('Skipped')),
            ('1', _('Failed')),
            ('2', _('Passed with warning')),
            ('3', _('Successful')),
        )

        widgets = {
            'result': forms.Select(choices=STATUS, attrs={'class': 'form-control'}),
            'test': HiddenInput(), 'protocol': HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': '4'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput(),
        }


class ResultNoteForm(ModelForm):
    class Meta:
        model = TestResultNote
        labels = {
            'desc': _('Description'),
            'text': _('Text'),
            'format': _('Format'),
        }
        fields = '__all__'
        FORMAT = (
            (0, 'Textile'),
            (1, _('Code')),
        )
        widgets = {
            'result': HiddenInput(),
            'text': forms.Textarea(attrs={'rows': '15'}),
            'format': forms.Select(choices=FORMAT, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


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


class ResultImageForm(ModelForm):
    class Meta:
        model = TestResultImage
        labels = {
            'image': _('Image'),
            'width': _('Width'),
            'height': _('Height'),
        }
        fields = '__all__'
        widgets = {
            'result': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ResultFileForm(ModelForm):
    class Meta:
        model = TestResultFile
        labels = {
            'file': _('File'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {
            'result': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ResultIssueForm(ModelForm):
    class Meta:
        model = TestResultIssue
        labels = {
            'text': _('Text'),
            'ticket': _('Ticket'),
        }
        fields = '__all__'
        widgets = {
            'result': HiddenInput(),
            'text': forms.Textarea(attrs={'rows': '4'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
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


class ProtocolFileForm(ModelForm):
    class Meta:
        model = ProtocolFile
        labels = {
            'type': _('Type'),
            'desc': _('Description'),
            'file': _('File'),
        }
        fields = '__all__'
        TYPE = (
            (0, _('Firmware')),
            (1, _('Docx Protocol')),
            (2, _('Scan-copy Protocol')),
        )
        widgets = {
            'protocol': HiddenInput(),
            'type': forms.Select(choices=TYPE, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ProtocolAdditionalIssueForm(ModelForm):
    class Meta:
        model = ProtocolAdditionalIssue
        labels = {
            'text': _('Text'),
            'ticket': _('Ticket'),
        }
        fields = '__all__'
        widgets = {
            'protocol': HiddenInput(),
            'priority': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
