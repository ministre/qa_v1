from django.forms import ModelForm, HiddenInput
from device.models import DeviceType, Device
from django.utils.translation import gettext_lazy as _


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'name': _('Name'),
            'redmine_project': _('Redmine Project'),
            'redmine_project_name': _('Redmine Project Name'),
            'redmine_parent': _('Redmine Parent Project'),
        }
        fields = '__all__'
        widgets = {'created_by': HiddenInput(), 'created_at': HiddenInput(),
                   'updated_by': HiddenInput(), 'updated_at': HiddenInput()}


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        labels = {
            'project_id': _('Project ID'),
            'type': _('Device Type'),
            'vendor': _('Vendor'),
            'model': _('Model'),
            'hw': _('Hardware Version'),
            'interfaces': _('Interfaces'),
            'leds': _('Leds'),
            'buttons': _('Buttons'),
            'chipsets': _('Chipsets'),
            'memory': _('Memory'),
        }
        fields = '__all__'
