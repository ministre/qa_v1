from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TestplanPattern, CategoryPattern
from .forms import TestplanPatternForm, CategoryPatternForm
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from device.views import Item


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
def testplan_pattern_details(request, pk, tab_id: int):
    testplan_pattern = get_object_or_404(TestplanPattern, id=pk)
    return render(request, 'testplan_pattern/testplan_pattern_details.html', {'testplan_pattern': testplan_pattern,
                                                                              'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class CategoryPatternCreate(CreateView):
    model = CategoryPattern
    form_class = CategoryPatternForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'testplan_pattern': self.kwargs.get('testplan_pattern_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_pattern_details', kwargs={'pk': self.kwargs.get('testplan_pattern_id'),
                                                                          'tab_id': 2})
        return context

    def get_success_url(self):
        category = CategoryPattern.objects.filter(testplan_pattern=self.object.testplan_pattern).latest('priority')
        priority = category.priority + 1
        Item.set_priority(foo=self.object, priority=priority)
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.testplan_pattern, user=self.request.user)
        return reverse('testplan_pattern_details', kwargs={'pk': self.object.testplan_pattern.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class CategoryPatternUpdate(UpdateView):
    model = CategoryPattern
    form_class = CategoryPatternForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('category_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.testplan_pattern, user=self.request.user)
        return reverse('category_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class CategoryPatternDelete(DeleteView):
    model = CategoryPattern
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('category_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.testplan_pattern, user=self.request.user)
        return reverse('testplan_pattern_details', kwargs={'pk': self.object.testplan_pattern.id, 'tab_id': 2})


@login_required
def category_pattern_details(request, pk, tab_id: int):
    category_pattern = get_object_or_404(CategoryPattern, id=pk)
    return render(request, 'testplan_pattern/category_pattern_details.html', {'category_pattern': category_pattern,
                                                                              'tab_id': tab_id})
