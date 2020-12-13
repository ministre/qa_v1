from django.forms import ModelForm, HiddenInput
from store.models import Item
from django.utils.translation import gettext_lazy as _


class ItemForm(ModelForm):
    class Meta:
        model = Item
        labels = {
            'name': _('Name'),
            'location': _('Location'),
            'comment': _('Comment'),
        }
        fields = '__all__'
#        widgets = {
#            'date_of_received': HiddenInput(), 'received_by': HiddenInput(),
#            'date_of_returned': HiddenInput(), 'returned_by': HiddenInput()
#        }
