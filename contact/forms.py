from django.forms import ModelForm, HiddenInput
from contact.models import Contact
from django.utils.translation import gettext_lazy as _


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        labels = {
            'last_name': _('Last Name'),
            'first_name': _('First Name'),
            'middle_name': _('Middle Name'),
            'position': _('Position'),
            'email': _('E-mail'),
            'phone': _('Phone'),
            'vendor': _('Vendor'),
            'username': _('Username'),
        }
        fields = '__all__'
        widgets = {
            'created_by': HiddenInput(), 'created_at': HiddenInput(),
            'updated_by': HiddenInput(), 'updated_at': HiddenInput()
        }
