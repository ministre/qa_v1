from django.forms import ModelForm, HiddenInput
from .models import TestPlan, Category, Test, TestConfig, TestImage, TestFile, TestLink, TestComment
from testplan_pattern.models import TestPatternConfig, TestPatternImage, TestPatternFile, TestPatternLink, \
    TestPatternComment
from django.utils.translation import gettext_lazy as _
from django import forms
from django.shortcuts import get_object_or_404


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


class TestConfigForm(ModelForm):
    class Meta:
        model = TestConfig
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
            'test': HiddenInput(),
            'parent': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestImageForm(ModelForm):
    class Meta:
        model = TestImage
        labels = {
            'desc': _('Description'),
            'image': _('Image'),
            'width': _('Width'),
            'height': _('Height'),
        }
        fields = '__all__'
        widgets = {
            'test': HiddenInput(),
            'parent': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestFileForm(ModelForm):
    class Meta:
        model = TestFile
        labels = {
            'desc': _('Description'),
            'file': _('File'),
        }
        fields = '__all__'
        widgets = {
            'test': HiddenInput(),
            'parent': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestLinkForm(ModelForm):
    class Meta:
        model = TestLink
        labels = {
            'desc': _('Description'),
            'url': _('URL'),
        }
        fields = '__all__'
        widgets = {
            'test': HiddenInput(),
            'parent': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestCommentForm(ModelForm):
    class Meta:
        model = TestComment
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
            'test': HiddenInput(),
            'parent': HiddenInput(),
            'format': forms.Select(choices=FORMAT, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class TestAddConfigForm(forms.Form):
    test_id = forms.IntegerField()
    parent_config = forms.ModelChoiceField(queryset=TestPatternConfig.objects.all(), label=_('Pattern'),
                                           required=False)

    def __init__(self, *args, **kwargs):
        test_id = kwargs.pop('test_id', None)
        super(TestAddConfigForm, self).__init__(*args, **kwargs)
        self.fields['test_id'].initial = test_id
        test = get_object_or_404(Test, id=test_id)
        self.fields['parent_config'].queryset = TestPatternConfig.objects.filter(test_pattern=test.parent).order_by('id')
        self.fields['test_id'].widget = forms.HiddenInput()


class TestAddImageForm(forms.Form):
    test_id = forms.IntegerField()
    parent_image = forms.ModelChoiceField(queryset=TestPatternImage.objects.all(), label=_('Pattern'),
                                          required=False)

    def __init__(self, *args, **kwargs):
        test_id = kwargs.pop('test_id', None)
        super(TestAddImageForm, self).__init__(*args, **kwargs)
        self.fields['test_id'].initial = test_id
        test = get_object_or_404(Test, id=test_id)
        self.fields['parent_image'].queryset = TestPatternImage.objects.filter(test_pattern=test.parent).order_by('id')
        self.fields['test_id'].widget = forms.HiddenInput()


class TestAddFileForm(forms.Form):
    test_id = forms.IntegerField()
    parent_file = forms.ModelChoiceField(queryset=TestPatternFile.objects.all(), label=_('Pattern'),
                                         required=False)

    def __init__(self, *args, **kwargs):
        test_id = kwargs.pop('test_id', None)
        super(TestAddFileForm, self).__init__(*args, **kwargs)
        self.fields['test_id'].initial = test_id
        test = get_object_or_404(Test, id=test_id)
        self.fields['parent_file'].queryset = TestPatternFile.objects.filter(test_pattern=test.parent).order_by('id')
        self.fields['test_id'].widget = forms.HiddenInput()


class TestAddLinkForm(forms.Form):
    test_id = forms.IntegerField()
    parent_link = forms.ModelChoiceField(queryset=TestPatternLink.objects.all(), label=_('Pattern'),
                                         required=False)

    def __init__(self, *args, **kwargs):
        test_id = kwargs.pop('test_id', None)
        super(TestAddLinkForm, self).__init__(*args, **kwargs)
        self.fields['test_id'].initial = test_id
        test = get_object_or_404(Test, id=test_id)
        self.fields['parent_link'].queryset = TestPatternLink.objects.filter(test_pattern=test.parent).order_by('id')
        self.fields['test_id'].widget = forms.HiddenInput()


class TestAddCommentForm(forms.Form):
    test_id = forms.IntegerField()
    parent_comment = forms.ModelChoiceField(queryset=TestPatternComment.objects.all(), label=_('Pattern'),
                                            required=False)

    def __init__(self, *args, **kwargs):
        test_id = kwargs.pop('test_id', None)
        super(TestAddCommentForm, self).__init__(*args, **kwargs)
        self.fields['test_id'].initial = test_id
        test = get_object_or_404(Test, id=test_id)
        self.fields['parent_comment'].queryset = TestPatternComment.objects.filter(test_pattern=test.parent).order_by('id')
        self.fields['test_id'].widget = forms.HiddenInput()
