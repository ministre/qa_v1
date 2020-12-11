from django.forms import ModelForm
from device.models import DeviceType, Device


class DeviceTypeForm(ModelForm):
    class Meta:
        model = DeviceType
        labels = {
            'main_type': 'Тип (имя корневого проекта Redmine)',
            'sub_type': 'Подтип (хэштег проекта Redmine)',
            'name': 'Описание',
        }
        fields = ['main_type', 'sub_type', 'name']

    def __init__(self, *args, **kwargs):
        super(DeviceTypeForm, self).__init__(*args, **kwargs)
        self.fields['sub_type'].required = False


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
        fields = ['project_id', 'vendor', 'model', 'hw', 'interfaces', 'leds', 'buttons', 'chipsets', 'memory']

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['hw'].required = False
        self.fields['interfaces'].required = False
        self.fields['leds'].required = False
        self.fields['buttons'].required = False
        self.fields['chipsets'].required = False
        self.fields['memory'].required = False
