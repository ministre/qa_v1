from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from contact.models import Contact
from contact.forms import ContactForm
from django.urls import reverse
from django.utils import timezone


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    context_object_name = 'contacts'
    queryset = Contact.objects.all().order_by('last_name')
    template_name = 'contact/contacts.html'


@method_decorator(login_required, name='dispatch')
class ContactCreate(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('contacts')
        return context

    def get_success_url(self):
        return reverse('contacts')


@method_decorator(login_required, name='dispatch')
class ContactUpdate(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('contacts')
        return context

    def get_success_url(self):
        return reverse('contacts')


@method_decorator(login_required, name='dispatch')
class ContactDelete(DeleteView):
    model = Contact
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('contacts')
        return context

    def get_success_url(self):
        return reverse('contacts')
