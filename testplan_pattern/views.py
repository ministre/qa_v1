from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TestplanPattern, CategoryPattern, TestPattern
from testplan.models import Test
from .forms import TestplanPatternForm, CategoryPatternForm, TestPatternForm, TestNamesUpdateForm, \
    TestPurposesUpdateForm
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from device.views import Item
from django.http import HttpResponseRedirect
from django.db.models import Max, Min
import textile
from django.utils.translation import gettext_lazy as _


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
    tests_count = testplan_pattern.tests_count()
    testplans = testplan_pattern.get_subs()
    return render(request, 'testplan_pattern/testplan_pattern_details.html', {'testplan_pattern': testplan_pattern,
                                                                              'tests_count': tests_count,
                                                                              'testplans': testplans,
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
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

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


@login_required
def category_pattern_up(request, pk):
    cat = get_object_or_404(CategoryPattern, id=pk)
    pre_cat6s = CategoryPattern.objects.filter(testplan_pattern=cat.testplan_pattern,
                                               priority__lt=cat.priority).aggregate(Max('priority'))
    pre_cat = get_object_or_404(CategoryPattern, testplan_pattern=cat.testplan_pattern,
                                priority=pre_cat6s['priority__max'])
    Item.set_priority(foo=pre_cat, priority=cat.priority)
    Item.set_priority(foo=cat, priority=pre_cat6s['priority__max'])
    return HttpResponseRedirect(reverse('testplan_pattern_details', kwargs={'pk': cat.testplan_pattern.id,
                                                                            'tab_id': 2}))


@login_required
def category_pattern_down(request, pk):
    cat = get_object_or_404(CategoryPattern, id=pk)
    next_cat6s = CategoryPattern.objects.filter(testplan_pattern=cat.testplan_pattern,
                                                priority__gt=cat.priority).aggregate(Min('priority'))
    next_cat = get_object_or_404(CategoryPattern, testplan_pattern=cat.testplan_pattern,
                                 priority=next_cat6s['priority__min'])
    Item.set_priority(foo=next_cat, priority=cat.priority)
    Item.set_priority(foo=cat, priority=next_cat6s['priority__min'])
    return HttpResponseRedirect(reverse('testplan_pattern_details', kwargs={'pk': cat.testplan_pattern.id,
                                                                            'tab_id': 2}))


@method_decorator(login_required, name='dispatch')
class TestPatternCreate(CreateView):
    model = TestPattern
    form_class = TestPatternForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'category_pattern': self.kwargs.get('category_pattern_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_pattern = get_object_or_404(CategoryPattern, id=self.kwargs.get('category_pattern_id'))
        context['back_url'] = reverse('testplan_pattern_details', kwargs={'pk': category_pattern.testplan_pattern.id,
                                                                          'tab_id': 2})
        return context

    def get_success_url(self):
        test_pattern = TestPattern.objects.filter(category_pattern=self.object.category_pattern).latest('priority')
        priority = test_pattern.priority + 1
        Item.set_priority(foo=self.object, priority=priority)
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.category_pattern, user=self.request.user)
        Item.update_timestamp(foo=self.object.category_pattern.testplan_pattern, user=self.request.user)
        return reverse('testplan_pattern_details', kwargs={'pk': self.object.category_pattern.testplan_pattern.id,
                                                           'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class TestPatternUpdate(UpdateView):
    model = TestPattern
    form_class = TestPatternForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.category_pattern, user=self.request.user)
        Item.update_timestamp(foo=self.object.category_pattern.testplan_pattern, user=self.request.user)
        return reverse('test_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class TestPatternDelete(DeleteView):
    model = TestPattern
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_pattern_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.category_pattern, user=self.request.user)
        Item.update_timestamp(foo=self.object.category_pattern.testplan_pattern, user=self.request.user)
        return reverse('testplan_pattern_details', kwargs={'pk': self.object.category_pattern.testplan_pattern.id,
                                                           'tab_id': 2})


@login_required
def test_pattern_details(request, pk, tab_id: int):
    test_pattern = get_object_or_404(TestPattern, id=pk)
    num = test_pattern.get_num()
    procedure = textile.textile(test_pattern.procedure)
    expected = textile.textile(test_pattern.expected)
    test_names_update_form = TestNamesUpdateForm(initial={'name': test_pattern.name}, pattern_id=test_pattern.id)
    test_purposes_update_form = TestPurposesUpdateForm(initial={'purpose': test_pattern.purpose},
                                                       pattern_id=test_pattern.id)
    return render(request, 'testplan_pattern/test_pattern_details.html', {'test_pattern': test_pattern, 'num': num,
                                                                          'test_names_update_form':
                                                                              test_names_update_form,
                                                                          'test_purposes_update_form':
                                                                              test_purposes_update_form,
                                                                          'procedure': procedure, 'expected': expected,
                                                                          'tab_id': tab_id})


@login_required
def test_pattern_up(request, pk):
    test = get_object_or_404(TestPattern, id=pk)
    pre_tests = TestPattern.objects.filter(category_pattern=test.category_pattern,
                                           priority__lt=test.priority).aggregate(Max('priority'))
    pre_test = get_object_or_404(TestPattern, category_pattern=test.category_pattern,
                                 priority=pre_tests['priority__max'])
    Item.set_priority(foo=pre_test, priority=test.priority)
    Item.set_priority(foo=test, priority=pre_tests['priority__max'])
    return HttpResponseRedirect(reverse('testplan_pattern_details',
                                        kwargs={'pk': test.category_pattern.testplan_pattern.id, 'tab_id': 2}))


@login_required
def test_pattern_down(request, pk):
    test = get_object_or_404(TestPattern, id=pk)
    next_tests = TestPattern.objects.filter(category_pattern=test.category_pattern,
                                            priority__gt=test.priority).aggregate(Min('priority'))
    next_test = get_object_or_404(TestPattern, category_pattern=test.category_pattern,
                                  priority=next_tests['priority__min'])
    Item.set_priority(foo=next_test, priority=test.priority)
    Item.set_priority(foo=test, priority=next_tests['priority__min'])
    return HttpResponseRedirect(reverse('testplan_pattern_details',
                                        kwargs={'pk': test.category_pattern.testplan_pattern.id, 'tab_id': 2}))


@login_required
def test_names_update(request):
    if request.method == "POST":
        test_pattern = get_object_or_404(TestPattern, id=request.POST['pattern_id'])
        back_url = reverse('test_pattern_details', kwargs={'pk': test_pattern.id, 'tab_id': 3})
        form = TestNamesUpdateForm(request.POST, pattern_id=test_pattern.id)
        if form.is_valid():
            test_pattern.name = request.POST['name']
            test_pattern.save()
            for test_id in form.cleaned_data.get('tests'):
                test = get_object_or_404(Test, id=test_id)
                test.name = request.POST['name']
                test.save()
            return render(request, 'device/message.html', {'message': [True, _('Update successful')],
                                                           'back_url': back_url})
        return HttpResponseRedirect(reverse('test_pattern_details', kwargs={'pk': test_pattern.id,
                                                                            'tab_id': 3}))
    else:
        back_url = reverse('testplan_patterns')
        return render(request, 'device/message.html', {'message': [False, _('Page not found')], 'back_url': back_url})


@login_required
def test_purposes_update(request):
    if request.method == "POST":
        test_pattern = get_object_or_404(TestPattern, id=request.POST['pattern_id'])
        back_url = reverse('test_pattern_details', kwargs={'pk': test_pattern.id, 'tab_id': 3})
        form = TestPurposesUpdateForm(request.POST, pattern_id=test_pattern.id)
        if form.is_valid():
            test_pattern.purpose = request.POST['purpose']
            test_pattern.save()
            for test_id in form.cleaned_data.get('tests'):
                test = get_object_or_404(Test, id=test_id)
                test.purpose = request.POST['purpose']
                test.save()
            return render(request, 'device/message.html', {'message': [True, _('Update successful')],
                                                           'back_url': back_url})
        return HttpResponseRedirect(reverse('test_pattern_details', kwargs={'pk': test_pattern.id,
                                                                            'tab_id': 3}))
    else:
        back_url = reverse('testplan_patterns')
        return render(request, 'device/message.html', {'message': [False, _('Page not found')], 'back_url': back_url})
