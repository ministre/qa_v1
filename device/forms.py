from django.forms import ModelForm
from device.models import DeviceType, Device
from django.utils.translation import gettext_lazy as _


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'main_type': _('Type'),
            'sub_type': _('Subtype'),
            'name': _('Description'),
        }
        fields = '__all__'


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
