from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TestplanPattern
from .forms import TestplanPatternForm
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404


@method_decorator(login_required, name='dispatch')
class TestplanPatternListView(ListView):
    context_object_name = 'testplan_patterns'
    queryset = TestplanPattern.objects.all().order_by("name")
    template_name = 'testplan_pattern/testplan_patterns.html'


@method_decorator(login_required, name='dispatch')
class TestplanPatternCreate(CreateView):
    model = TestplanPattern
    form_class = TestplanPatternForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_patterns')
        return context

    def get_success_url(self):
        return reverse('testplan_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class TestplanPatternUpdate(UpdateView):
    model = TestplanPattern
    form_class = TestplanPatternForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('testplan_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class TestplanPatternDelete(DeleteView):
    model = TestplanPattern
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('testplan_patterns')


@login_required
def testplan_details(request, pk, tab_id):
    testplan_pattern = get_object_or_404(TestplanPattern, id=pk)
    return render(request, 'testplan_pattern/testplan_pattern_details.html', {'testplan_pattern': testplan_pattern,
                                                                              'tab_id': tab_id})
