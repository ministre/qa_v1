from django.contrib.auth.decorators import login_required
from store.models import Item
from .forms import ItemForm
from django.http import HttpResponseRedirect
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse


@method_decorator(login_required, name='dispatch')
class ItemListView(ListView):
    context_object_name = 'items'
    queryset = Item.objects.all().order_by("-id")
    template_name = 'store/items.html'


@method_decorator(login_required, name='dispatch')
class ItemCreate(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'store/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('items')
        return context

    def get_success_url(self):
        return reverse('items')


@method_decorator(login_required, name='dispatch')
class ItemUpdate(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'store/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('items')
        return context

    def get_success_url(self):
        return reverse('items')


@method_decorator(login_required, name='dispatch')
class ItemDelete(DeleteView):
    model = Item
    template_name = 'store/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('items')
        return context

    def get_success_url(self):
        return reverse('items')


@login_required
def item_return(request, pk):
    item = Item.objects.get(id=pk)
    item.location = ''
    item.returned_by = request.user
    item.date_of_returned = datetime.now()
    item.save()
    return HttpResponseRedirect(reverse('items'))
