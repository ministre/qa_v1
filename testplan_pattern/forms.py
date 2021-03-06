from django.forms import ModelForm, HiddenInput
from .models import TestplanPattern, CategoryPattern, TestPattern, TestPatternConfig, TestPatternImage, \
    TestPatternFile, TestPatternLink, TestPatternComment, TestPatternValueInteger, TestPatternValueIntegerPair, \
    TestPatternValueText
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

    def __init__(self, *args, **kwargs):
        super(TestPatternForm, self).__init__(*args, **kwargs)
        self.fields['device_types'].widget.attrs = {'size': 35}


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


class TestPatternConfigForm(ModelForm):
    class Meta:
        model = TestPatternConfig
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
            'lang': forms.Select(choices=LANG, attrs={'class': 'form-control'}),
            'test_pattern': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestPatternImageForm(ModelForm):
    class Meta:
        model = TestPatternImage
        labels = {
            'desc': _('Description'),
            'image': _('Image'),
            'width': _('Width'),
            'height': _('Height'),
        }
        fields = '__all__'
        widgets = {
            'test_pattern': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestPatternFileForm(ModelForm):
    class Meta:
        model = TestPatternFile
        labels = {
            'desc': _('Description'),
            'file': _('File'),
        }
        fields = '__all__'
        widgets = {
            'test_pattern': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestPatternLinkForm(ModelForm):
    class Meta:
        model = TestPatternLink
        labels = {
            'desc': _('Description'),
            'url': _('URL'),
        }
        fields = '__all__'
        widgets = {
            'test_pattern': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestPatternCommentForm(ModelForm):
    class Meta:
        model = TestPatternComment
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
            'test_pattern': HiddenInput(),
            'text': forms.Textarea(attrs={'rows': '15'}),
            'format': forms.Select(choices=FORMAT, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestPatternValueIntegerForm(ModelForm):
    class Meta:
        model = TestPatternValueInteger
        labels = {
            'desc': _('Description'),
            'unit': _('Unit'),
        }
        fields = '__all__'
        widgets = {
            'test_pattern': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestPatternValueIntegerPairForm(ModelForm):
    class Meta:
        model = TestPatternValueIntegerPair
        labels = {
            'desc': _('Description'),
            'unit1': _('Unit 1'),
            'unit2': _('Unit 2'),
        }
        fields = '__all__'
        widgets = {
            'test_pattern': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestPatternValueTextForm(ModelForm):
    class Meta:
        model = TestPatternValueText
        labels = {
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {
            'test_pattern': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
