from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, HiddenInput
from docx_builder.models import DocxProfile


class DocxProfileForm(ModelForm):
    class Meta:
        model = DocxProfile
        labels = {
            'name': _('Name'),
            'type': _('Type'),
            'header_text1': _('Header Text 1'),
            'header_text2': _('Header Text 2'),
            'title_font_name': _('Title Font Name'),
            'title_font_size': _('Title Font Size') + ', [10-40]',
            'title_font_bold': _('Title Font Bold'),
            'title_font_italic': _('Title Font Italic'),
            'title_font_underline': _('Title Font Underline'),
            'title_font_color_red': _('Title Font Color Red') + ', [0-255]',
            'title_font_color_green': _('Title Font Color Green') + ', [0-255]',
            'title_font_color_blue': _('Title Font Color Blue') + ', [0-255]',
            'title_space_before': _('Title Space Before') + ', [0-40]',
            'title_space_after': _('Title Space After') + ', [0-40]',
            'title_alignment': _('Title Alignment'),
            'h1_font_name': _('Heading 1 Font Name'),
            'h1_font_size': _('Heading 1 Font Size') + ', [10-40]',
            'h1_font_bold': _('Heading 1 Font Bold'),
            'h1_font_italic': _('Heading 1 Font Italic'),
            'h1_font_underline': _('Heading 1 Font Underline'),
            'h1_font_color_red': _('Heading 1 Font Red') + ', [0-255]',
            'h1_font_color_green': _('Heading 1 Font Green') + ', [0-255]',
            'h1_font_color_blue': _('Heading 1 Font Blue') + ', [0-255]',
            'h1_space_before': _('Heading 1 Space Font Before') + ', [0-40]',
            'h1_space_after': _('Heading 1 Space Font After') + ', [0-40]',
            'h1_alignment': _('Heading 1 Alignment'),
            'h2_font_name': _('Heading 2 Font Name'),
            'h2_font_size': _('Heading 2 Font Size') + ', [10-40]',
            'h2_font_bold': _('Heading 2 Font Bold'),
            'h2_font_italic': _('Heading 2 Font Italic'),
            'h2_font_underline': _('Heading 2 Font Underline'),
            'h2_font_color_red': _('Heading 2 Font Color Red') + ', [0-255]',
            'h2_font_color_green': _('Heading 2 Font Color Green') + ', [0-255]',
            'h2_font_color_blue': _('Heading 2 Font Color Blue') + ', [0-255]',
            'h2_space_before': _('Heading 2 Space Before') + ', [0-40]',
            'h2_space_after': _('Heading 2 Space After') + ', [0-40]',
            'h2_alignment': _('Heading 2 Alignment'),
        }
        fields = '__all__'
        TYPE = (
            (0, _('Protocol')),
            (1, _('Detailed Protocol')),
            (2, _('Testplan')),
            (3, _('Technical requirements')),
        )
        FONTNAME = (
            ('Calibri', 'Calibri'),
            ('Cambria', 'Cambria'),
        )
        ALIGNMENT = (
            (0, 'Left'),
            (1, 'Center'),
            (2, 'Right'),
            (3, 'Justify'),
        )
        widgets = {
            'type': forms.Select(choices=TYPE, attrs={'class': 'form-control'}),
            'title_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'title_font_bold': forms.CheckboxInput(),
            'title_font_italic': forms.CheckboxInput(),
            'title_font_underline': forms.CheckboxInput(),
            'title_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),
            'h1_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'h1_font_bold': forms.CheckboxInput(),
            'h1_font_italic': forms.CheckboxInput(),
            'h1_font_underline': forms.CheckboxInput(),
            'h1_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),
            'h2_font_name': forms.Select(choices=FONTNAME, attrs={'class': 'form-control'}),
            'h2_font_bold': forms.CheckboxInput(),
            'h2_font_italic': forms.CheckboxInput(),
            'h2_font_underline': forms.CheckboxInput(),
            'h2_alignment': forms.Select(choices=ALIGNMENT, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput(),
        }


class BuildDocxProtocolForm(forms.Form):
    protocol_id = forms.IntegerField()
    docx_profile_id = forms.ModelChoiceField(queryset=DocxProfile.objects.filter(type=0).order_by('id'),
                                             label=_('Docx Profile'))
    title_page = forms.BooleanField(label=_('Title page'), required=False, initial=True)
    header = forms.BooleanField(label=_('Header'), required=False, initial=True)
    general = forms.BooleanField(label=_('Device information'), required=False, initial=True)
    performance = forms.BooleanField(label=_('Performance results'), required=False, initial=True)
    results_table = forms.BooleanField(label=_('Test results'), required=False, initial=True)
    summary = forms.BooleanField(label=_('Summary'), required=False, initial=True)
    team = forms.BooleanField(label=_('Testing team'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(BuildDocxProtocolForm, self).__init__(*args, **kwargs)
        self.fields['protocol_id'].widget = forms.HiddenInput()


class BuildDocxProtocolDetailedForm(forms.Form):
    protocol_id = forms.IntegerField()
    docx_profile_id = forms.ModelChoiceField(queryset=DocxProfile.objects.filter(type=1).order_by('id'),
                                             label=_('Docx Profile'))

    def __init__(self, *args, **kwargs):
        super(BuildDocxProtocolDetailedForm, self).__init__(*args, **kwargs)
        self.fields['protocol_id'].widget = forms.HiddenInput()
