from django.forms import ModelForm
from store.models import Item
from django import forms


class ItemForm(ModelForm):
    class Meta:
        model = Item
        # widgets = {'received_by': forms.HiddenInput()}
        labels = {
            'name': 'Наименование',
            'location': 'Где лежит/номер полки',
            'comment': 'Комментарий',
        }
        fields = ['name', 'location', 'comment']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['location'].required = True
        self.fields['comment'].required = False
