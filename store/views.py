from django.contrib.auth.decorators import login_required
from store.models import Item
from .forms import ItemForm
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render


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

    def get_initial(self):
        return {'received_by': self.request.user}

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
def item_return(request):
    if request.method == "POST":
        item = get_object_or_404(Item, id=request.POST['item_id'])
        item.location = None
        item.returned_by = request.user
        item.date_of_returned = timezone.now()
        item.save()
        return HttpResponseRedirect(reverse('items'))
    else:
        message = [False, _('Page not found')]
        return render(request, 'docx_generator/message.html', {'message': message})
