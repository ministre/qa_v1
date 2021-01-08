from django.forms import ModelForm, HiddenInput
from device.models import Vendor, DeviceType, Device, DevicePhoto, DeviceSample, DeviceSampleAccount
from django.utils.translation import gettext_lazy as _


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
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
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
