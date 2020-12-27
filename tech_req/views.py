from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TechReq, TechReqFile
from .forms import TechReqForm, TechReqFileForm
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from device.views import Item


@method_decorator(login_required, name='dispatch')
class TechReqListView(ListView):
    context_object_name = 'tech_reqs'
    queryset = TechReq.objects.all().order_by('name')
    template_name = 'tech_req/tech_reqs.html'


@method_decorator(login_required, name='dispatch')
class TechReqCreate(CreateView):
    model = TechReq
    form_class = TechReqForm
    template_name = 'tech_req/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('tech_reqs')
        return context

    def get_success_url(self):
        return reverse('tech_reqs')


@method_decorator(login_required, name='dispatch')
class TechReqUpdate(UpdateView):
    model = TechReq
    form_class = TechReqForm
    template_name = 'tech_req/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('tech_req_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('tech_req_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class TechReqDelete(DeleteView):
    model = TechReq
    template_name = 'tech_req/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('tech_req_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('tech_reqs')


@login_required
def tech_req_details(request, pk, tab_id):
    tech_req = get_object_or_404(TechReq, id=pk)
    return render(request, 'tech_req/tech_req_details.html', {'tech_req': tech_req, 'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class TechReqFileCreate(CreateView):
    model = TechReqFile
    form_class = TechReqFileForm
    template_name = 'tech_req/create.html'

    def get_initial(self):
        return {'tech_req': self.kwargs.get('tech_req_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('tech_req_details', kwargs={'pk': self.kwargs.get('tech_req_id'), 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.tech_req, user=self.request.user)
        return reverse('tech_req_details', kwargs={'pk': self.object.tech_req.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class TechReqFileUpdate(UpdateView):
    model = TechReqFile
    form_class = TechReqFileForm
    template_name = 'tech_req/update.html'

    def get_initial(self):
        return {'tech_req': self.object.tech_req.id,
                'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('tech_req_details', kwargs={'pk': self.object.tech_req.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.tech_req, user=self.request.user)
        return reverse('tech_req_details', kwargs={'pk': self.object.tech_req.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class TechReqFileDelete(DeleteView):
    model = TechReqFile
    template_name = 'tech_req/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('tech_req_details', kwargs={'pk': self.object.tech_req.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.tech_req, user=self.request.user)
        return reverse('tech_req_details', kwargs={'pk': self.object.tech_req.id, 'tab_id': 2})
