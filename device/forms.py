from django.forms import ModelForm, HiddenInput
from device.models import Vendor, DeviceType, Device, DevicePhoto, DeviceSample, DeviceSampleAccount, DeviceFile, \
    DeviceNote, DeviceContact, Chipset
from django.utils.translation import gettext_lazy as _
from django import forms


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        labels = {
            'name': _('Name'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'name': _('Name'),
            'redmine_project': _('Redmine Project'),
            'redmine_project_name': _('Redmine Project Name'),
            'redmine_project_desc': _('Redmine Project Description'),
            'redmine_parent': _('Redmine Parent Project'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput(),
                   'main_type': HiddenInput(), 'sub_type': HiddenInput()}


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        labels = {
            'type': _('Device Type'),
            'vendor': _('Vendor'),
            'model': _('Model'),
            'hw': _('Hardware Version'),
            'eol': _('EoL'),
            'redmine_project': _('Redmine Project'),
            'redmine_project_name': _('Redmine Project Name (leave blank to set Vendor + Model)'),
            'redmine_project_desc': _('Redmine Project Description'),
            'redmine_parent': _('Redmine Parent Project (leave blank to copy project ID from device type)'),
            'interfaces': _('Interfaces'),
            'leds': _('Leds'),
            'buttons': _('Buttons'),
            'chipsets': _('Chipsets'),
            'memory': _('Memory'),
        }
        fields = '__all__'
        widgets = {'chipsets': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DevicePhotoForm(ModelForm):
    class Meta:
        model = DevicePhoto
        labels = {
            'photo': _('Photo'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceSampleForm(ModelForm):
    class Meta:
        model = DeviceSample
        labels = {
            'sn': _('Serial Number'),
            'desc': _('Description'),
        }
        fields = '__all__'
        widgets = {'device': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceSampleAccountForm(ModelForm):
    class Meta:
        model = DeviceSampleAccount
        labels = {
            'username': _('Username'),
            'password': _('Password'),
        }
        fields = '__all__'
        widgets = {'sample': HiddenInput(),
                   'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceFileForm(ModelForm):
    class Meta:
        model = DeviceFile
        labels = {
            'type': _('Type'),
            'desc': _('Description'),
            'file': _('File'),
        }
        fields = '__all__'
        TYPE = (
            (0, _('Datasheet')),
            (1, _('Quick Installation Guide')),
            (2, _('HowTo')),
            (3, _('Certificate')),
            (4, _('Other')),
        )
        widgets = {
            'device': HiddenInput(),
            'type': forms.Select(choices=TYPE, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class DeviceNoteForm(ModelForm):
    class Meta:
        model = DeviceNote
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
            'device': HiddenInput(),
            'text': forms.Textarea(attrs={'rows': '15'}),
            'format': forms.Select(choices=FORMAT, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class DeviceContactForm(ModelForm):
    class Meta:
        model = DeviceContact
        labels = {
            'contact': _('Contact'),
        }
        fields = '__all__'
        widgets = {
            'device': HiddenInput(),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }


class ChipsetForm(ModelForm):
    class Meta:
        model = Chipset
        labels = {
            'vendor': _('Vendor'),
            'model': _('Model'),
            'type': _('Type'),
            'desc': _('Description'),
            'datasheet': _('Datasheet'),
        }
        fields = '__all__'
        TYPE = (
            (0, 'SoC'),
            (1, 'SoC + Wi-Fi 2.4 GHz'),
            (2, 'SoC + Wi-Fi 5 GHz'),
            (3, 'SoC + Wi-Fi Dual Band'),
            (4, 'Wi-Fi 2.4 GHz'),
            (5, 'Wi-Fi 5 GHz'),
            (6, 'Wi-Fi Dual Band'),
            (7, 'Mobile Modem'),
            (8, 'VoIP'),
            (9, 'Ethernet Switch'),
            (10, 'xDSL Modem'),
            (11, 'Z-Wave'),
        )
        widgets = {
            'type': forms.Select(choices=TYPE, attrs={'class': 'form-control'}),
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
