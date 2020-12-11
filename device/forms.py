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
            'project_id': 'Идентификатор проекта Redmine*',
            'vendor': 'Производитель*',
            'model': 'Модель*',
            'hw': 'Версия Hardware',
            'interfaces': 'Интерфейсы',
            'leds': 'Индикаторы',
            'buttons': 'Кнопки',
            'chipsets': 'Чипсеты',
            'memory': 'Память',
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['hw'].required = False
        self.fields['interfaces'].required = False
        self.fields['leds'].required = False
        self.fields['buttons'].required = False
        self.fields['chipsets'].required = False
        self.fields['memory'].required = False
