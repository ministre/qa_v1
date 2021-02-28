from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from qa_v1 import settings
from .models import TestPlan, Category, Test, TestConfig, TestImage, TestFile, TestLink, TestComment
from .forms import TestPlanForm, CategoryForm, TestForm, TestConfigForm, TestAddConfigForm, TestImageForm, \
    TestAddImageForm, TestFileForm, TestAddFileForm, TestLinkForm, TestAddLinkForm, TestCommentForm, TestAddCommentForm
from docx_builder.forms import BuildDocxTestplanForm
from redmine.forms import RedmineTestExportForm, RedmineTestplanExportForm
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import textile
from django import forms
from django.utils import timezone
from django.http import HttpResponseRedirect
from device.views import Item
from django.db.models import Max, Min
from testplan_pattern.models import CategoryPattern, TestPattern, TestPatternConfig, TestPatternImage, \
    TestPatternFile, TestPatternLink, TestPatternComment
from django.utils.datastructures import MultiValueDictKeyError


@method_decorator(login_required, name='dispatch')
class TestplanListView(ListView):
    context_object_name = 'testplans'
    queryset = TestPlan.objects.all().order_by("name")
    template_name = 'testplan/testplans.html'


@method_decorator(login_required, name='dispatch')
class TestplanCreate(CreateView):
    model = TestPlan
    form_class = TestPlanForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplans')
        return context

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class TestplanUpdate(UpdateView):
    model = TestPlan
    form_class = TestPlanForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class TestplanDelete(DeleteView):
    model = TestPlan
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('testplans')


@login_required
def testplan_details(request, pk, tab_id):
    testplan = get_object_or_404(TestPlan, id=pk)
    tests_count = testplan.tests_count()
    protocols = testplan.get_protocols()
    build_testplan_form = BuildDocxTestplanForm(initial={'testplan_id': testplan.id})
    export_form = RedmineTestplanExportForm(initial={'testplan_id': testplan.id,
                                                     'redmine_project': testplan.redmine_project,
                                                     'redmine_project_name': testplan.redmine_project_name,
                                                     'redmine_project_desc': testplan.redmine_project_desc,
                                                     'redmine_parent': testplan.redmine_parent})
    return render(request, 'testplan/testplan_details.html', {'testplan': testplan, 'tests_count': tests_count,
                                                              'protocols': protocols,
                                                              'build_testplan_form': build_testplan_form,
                                                              'redmine_url': settings.REDMINE_URL,
                                                              'export_form': export_form,
                                                              'tab_id': tab_id})


@login_required
def testplan_clone(request, pk):
    if request.method == 'POST':
        form = TestPlanForm(request.POST)
        if form.is_valid():
            new_testplan = TestPlan(name=request.POST['name'],
                                    version=request.POST['version'])
            new_testplan.save()
            src_testplan = get_object_or_404(TestPlan, id=request.POST['src_testplan'])
            src_tests = Test.objects.filter(testplan=src_testplan).order_by('id')
            for src_test in src_tests:
                new_test = Test(testplan=new_testplan, category=src_test.category, url=src_test.url,
                                name=src_test.name, procedure=src_test.procedure, expected=src_test.expected)
                new_test.save()
            return HttpResponseRedirect(reverse('testplans'))
    else:
        testplan = get_object_or_404(TestPlan, id=pk)
        form = TestPlanForm(initial={'name': testplan.name,
                                     'version': testplan.version})
        return render(request, 'testplan/clone.html', {'form': form, 'tp_id': testplan.id})


@login_required
def clear_tests(request, pk):
    testplan = get_object_or_404(TestPlan, id=pk)
    if request.method == 'POST':
        Category.objects.filter(testplan=testplan).delete()
        return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': pk, 'tab_id': 2}))
    else:
        back_url = reverse('testplan_details', kwargs={'pk': pk, 'tab_id': 2})
        message = _('Are you sure?')
        return render(request, 'testplan/clear.html', {'back_url': back_url, 'message': message})


@method_decorator(login_required, name='dispatch')
class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'testplan': self.kwargs.get('testplan_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_form(self, form_class=CategoryForm):
        form = super(CategoryCreate, self).get_form(form_class)
        testplan = get_object_or_404(TestPlan, id=self.kwargs.get('testplan_id'))
        if testplan.parent:
            form.fields['parent'].queryset = CategoryPattern.objects.filter(testplan_pattern=testplan.parent).order_by('priority')
        else:
            form.fields['parent'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplan_details', kwargs={'pk': self.kwargs.get('testplan_id'), 'tab_id': 2})
        return context

    def get_success_url(self):
        category = Category.objects.filter(testplan=self.object.testplan).latest('priority')
        priority = category.priority + 1
        Item.set_priority(foo=self.object, priority=priority)
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.testplan, user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_form(self, form_class=CategoryForm):
        form = super(CategoryUpdate, self).get_form(form_class)
        if self.object.testplan.parent:
            form.fields['parent'].queryset = CategoryPattern.objects.filter(testplan_pattern=self.object.testplan.parent).order_by('priority')
        else:
            form.fields['parent'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('category_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.testplan, user=self.request.user)
        return reverse('category_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class CategoryDelete(DeleteView):
    model = Category
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('category_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.testplan, user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.testplan.id, 'tab_id': 2})


@login_required
def category_details(request, pk, tab_id: int):
    category = get_object_or_404(Category, id=pk)
    return render(request, 'testplan/category_details.html', {'category': category, 'tab_id': tab_id})


@login_required
def category_up(request, pk):
    cat = get_object_or_404(Category, id=pk)
    pre_cat6s = Category.objects.filter(testplan=cat.testplan, priority__lt=cat.priority).aggregate(Max('priority'))
    pre_cat = get_object_or_404(Category, testplan=cat.testplan, priority=pre_cat6s['priority__max'])
    Item.set_priority(foo=pre_cat, priority=cat.priority)
    Item.set_priority(foo=cat, priority=pre_cat6s['priority__max'])
    return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': cat.testplan.id, 'tab_id': 2}))


@login_required
def category_down(request, pk):
    cat = get_object_or_404(Category, id=pk)
    next_cat6s = Category.objects.filter(testplan=cat.testplan, priority__gt=cat.priority).aggregate(Min('priority'))
    next_cat = get_object_or_404(Category, testplan=cat.testplan, priority=next_cat6s['priority__min'])
    Item.set_priority(foo=next_cat, priority=cat.priority)
    Item.set_priority(foo=cat, priority=next_cat6s['priority__min'])
    return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': cat.testplan.id, 'tab_id': 2}))


@method_decorator(login_required, name='dispatch')
class TestCreate(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'testplan/create.html'

    def get_initial(self):
        return {'cat': self.kwargs.get('category_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_form(self, form_class=TestForm):
        form = super(TestCreate, self).get_form(form_class)
        category = get_object_or_404(Category, id=self.kwargs.get('category_id'))
        if category.parent:
            form.fields['parent'].queryset = TestPattern.objects.filter(category_pattern=category.parent).order_by('priority')
        else:
            form.fields['parent'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, id=self.kwargs.get('category_id'))
        context['back_url'] = reverse('testplan_details', kwargs={'pk': category.testplan.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        test = Test.objects.filter(cat=self.object.cat).latest('priority')
        priority = test.priority + 1
        Item.set_priority(foo=self.object, priority=priority)
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.cat, user=self.request.user)
        Item.update_timestamp(foo=self.object.cat.testplan, user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.cat.testplan.id, 'tab_id': 2})


@method_decorator(login_required, name='dispatch')
class TestUpdate(UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'testplan/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_form(self, form_class=TestForm):
        form = super(TestUpdate, self).get_form(form_class)
        if self.object.cat.parent:
            form.fields['parent'].queryset = TestPattern.objects.filter(category_pattern=self.object.cat.parent).order_by('priority')
        else:
            form.fields['parent'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object, user=self.request.user)
        Item.update_timestamp(foo=self.object.cat, user=self.request.user)
        Item.update_timestamp(foo=self.object.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class TestDelete(DeleteView):
    model = Test
    template_name = 'testplan/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.cat, user=self.request.user)
        Item.update_timestamp(foo=self.object.cat.testplan, user=self.request.user)
        return reverse('testplan_details', kwargs={'pk': self.object.cat.testplan.id, 'tab_id': 2})


@login_required
def test_details(request, pk, tab_id):
    test = get_object_or_404(Test, id=pk)
    num = test.get_num()
    procedure = textile.textile(test.procedure)
    expected = textile.textile(test.expected)
    add_config_form = TestAddConfigForm(test_id=test.id)
    add_image_form = TestAddImageForm(test_id=test.id)
    add_file_form = TestAddFileForm(test_id=test.id)
    add_link_form = TestAddLinkForm(test_id=test.id)
    add_comment_form = TestAddCommentForm(test_id=test.id)
    export_form = RedmineTestExportForm(initial={'test_id': test.id,
                                                 'redmine_project': test.cat.testplan.redmine_project,
                                                 'redmine_wiki': test.redmine_wiki})
    return render(request, 'testplan/test_details.html', {'test': test, 'num': num, 'procedure': procedure,
                                                          'expected': expected,
                                                          'add_config_form': add_config_form,
                                                          'add_image_form': add_image_form,
                                                          'add_file_form': add_file_form,
                                                          'add_link_form': add_link_form,
                                                          'add_comment_form': add_comment_form,
                                                          'redmine_url': settings.REDMINE_URL,
                                                          'export_form': export_form,
                                                          'tab_id': tab_id})


@login_required
def test_up(request, pk):
    test = get_object_or_404(Test, id=pk)
    pre_tests = Test.objects.filter(cat=test.cat, priority__lt=test.priority).aggregate(Max('priority'))
    pre_test = get_object_or_404(Test, cat=test.cat, priority=pre_tests['priority__max'])
    Item.set_priority(foo=pre_test, priority=test.priority)
    Item.set_priority(foo=test, priority=pre_tests['priority__max'])
    return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': test.cat.testplan.id, 'tab_id': 2}))


@login_required
def test_down(request, pk):
    test = get_object_or_404(Test, id=pk)
    next_tests = Test.objects.filter(cat=test.cat, priority__gt=test.priority).aggregate(Min('priority'))
    next_test = get_object_or_404(Test, cat=test.cat, priority=next_tests['priority__min'])
    Item.set_priority(foo=next_test, priority=test.priority)
    Item.set_priority(foo=test, priority=next_tests['priority__min'])
    return HttpResponseRedirect(reverse('testplan_details', kwargs={'pk': test.cat.testplan.id, 'tab_id': 2}))


@login_required
def test_config_add(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test_id'])
        try:
            if request.POST['parent_config']:
                parent_config = get_object_or_404(TestPatternConfig, id=request.POST['parent_config'])
                TestConfig.objects.create(test=test, parent=parent_config, created_by=request.user,
                                          updated_by=request.user)
                return HttpResponseRedirect(reverse('test_details', kwargs={'pk': test.id, 'tab_id': 3}))

        except MultiValueDictKeyError:
            pass
        return HttpResponseRedirect(reverse('test_config_create', kwargs={'test_id': test.id}))

    else:
        return render(request, 'device/message.html', {'message': [False, _('Page not found')]})


@method_decorator(login_required, name='dispatch')
class TestConfigCreate(CreateView):
    model = TestConfig
    form_class = TestConfigForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestConfigUpdate(UpdateView):
    model = TestConfig
    form_class = TestConfigForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class TestConfigDelete(DeleteView):
    model = TestConfig
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 3})


@login_required
def test_image_add(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test_id'])
        try:
            if request.POST['parent_image']:
                parent_image = get_object_or_404(TestPatternImage, id=request.POST['parent_image'])
                TestImage.objects.create(test=test, parent=parent_image, created_by=request.user,
                                         updated_by=request.user)
                return HttpResponseRedirect(reverse('test_details', kwargs={'pk': test.id, 'tab_id': 4}))

        except MultiValueDictKeyError:
            pass
        return HttpResponseRedirect(reverse('test_image_create', kwargs={'test_id': test.id}))
    else:
        return render(request, 'device/message.html', {'message': [False, _('Page not found')]})


@method_decorator(login_required, name='dispatch')
class TestImageCreate(CreateView):
    model = TestImage
    form_class = TestImageForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class TestImageUpdate(UpdateView):
    model = TestImage
    form_class = TestImageForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class TestImageDelete(DeleteView):
    model = TestImage
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 4})


@login_required
def test_file_add(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test_id'])
        try:
            if request.POST['parent_file']:
                parent_file = get_object_or_404(TestPatternFile, id=request.POST['parent_file'])
                TestFile.objects.create(test=test, parent=parent_file, created_by=request.user,
                                        updated_by=request.user)
                return HttpResponseRedirect(reverse('test_details', kwargs={'pk': test.id, 'tab_id': 5}))

        except MultiValueDictKeyError:
            pass
        return HttpResponseRedirect(reverse('test_file_create', kwargs={'test_id': test.id}))
    else:
        return render(request, 'device/message.html', {'message': [False, _('Page not found')]})


@method_decorator(login_required, name='dispatch')
class TestFileCreate(CreateView):
    model = TestFile
    form_class = TestFileForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 5})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class TestFileUpdate(UpdateView):
    model = TestFile
    form_class = TestFileForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class TestFileDelete(DeleteView):
    model = TestFile
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 5})


@login_required
def test_link_add(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test_id'])
        try:
            if request.POST['parent_link']:
                parent_link = get_object_or_404(TestPatternLink, id=request.POST['parent_link'])
                TestLink.objects.create(test=test, parent=parent_link, created_by=request.user, updated_by=request.user)
                return HttpResponseRedirect(reverse('test_details', kwargs={'pk': test.id, 'tab_id': 6}))

        except MultiValueDictKeyError:
            pass
        return HttpResponseRedirect(reverse('test_link_create', kwargs={'test_id': test.id}))
    else:
        return render(request, 'device/message.html', {'message': [False, _('Page not found')]})


@method_decorator(login_required, name='dispatch')
class TestLinkCreate(CreateView):
    model = TestLink
    form_class = TestLinkForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestLinkUpdate(UpdateView):
    model = TestLink
    form_class = TestLinkForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class TestLinkDelete(DeleteView):
    model = TestLink
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 6})


@login_required
def test_comment_add(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test_id'])
        try:
            if request.POST['parent_comment']:
                parent_comment = get_object_or_404(TestPatternComment, id=request.POST['parent_comment'])
                TestComment.objects.create(test=test, parent=parent_comment, created_by=request.user,
                                           updated_by=request.user)
                return HttpResponseRedirect(reverse('test_details', kwargs={'pk': test.id, 'tab_id': 7}))

        except MultiValueDictKeyError:
            pass
        return HttpResponseRedirect(reverse('test_comment_create', kwargs={'test_id': test.id}))
    else:
        return render(request, 'device/message.html', {'message': [False, _('Page not found')]})


@method_decorator(login_required, name='dispatch')
class TestCommentCreate(CreateView):
    model = TestComment
    form_class = TestCommentForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'test': self.kwargs.get('test_id')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.kwargs.get('test_id'), 'tab_id': 7})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class TestCommentUpdate(UpdateView):
    model = TestComment
    form_class = TestCommentForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class TestCommentDelete(DeleteView):
    model = TestComment
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.test, user=self.request.user)
        Item.update_timestamp(foo=self.object.test.cat.testplan, user=self.request.user)
        return reverse('test_details', kwargs={'pk': self.object.test.id, 'tab_id': 7})


'''
@login_required
def test_import_details(request):
    if request.method == 'POST':
        test_id = request.POST['test_id']
        tag = request.POST['tag']
        project = get_project_and_keyword_from_test(test_id)[0]
        keyword = get_project_and_keyword_from_test(test_id)[1]
        test_details = parse_test_details_from_redmine(project, keyword, tag)
        Test.objects.filter(id=test_id).update(name=test_details[0], procedure=test_details[1],
                                               expected=test_details[2])
        return HttpResponseRedirect('/testplan/test/' + str(test_id) + '/')

def get_numbers_of_tests(tests):
    # генерируем нумерованный список тестов
    numbers_of_tests = []
    category = None
    i = 0
    j = 0
    for test in tests:
        new_category = test.category
        if new_category == category:
            j = j + 1
            numbers_of_tests.append(str(i) + '.' + str(j))
        else:
            i = i + 1
            j = 1
            numbers_of_tests.append(str(i) + '.' + str(j))
            category = test.category
    return numbers_of_tests

@login_required
def testplan_import(request, testplan_id):
    if request.method == 'POST':
        project_id = request.POST['project_id']
        tag = request.POST['tag']
        if project_id == '':
            error = 'Отсутствует индентификатор проекта!'
            return render(request, 'testplan/testplan_import_error.html', {'error': error, 'testplan_id': testplan_id})
        else:
            category = ''
            tests = []
            redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.1.1')
            # Получаем перечень тестов из Wiki страницы
            try:
                wiki_page = redmine.wiki_page.get('Wiki', project_id=project_id)
                blocks = wiki_page.text.split('h2. ')
                for i, block in enumerate(blocks):
                    if re.search('Программа и методика', block):
                        pm_blocks = blocks[i].split('\n')
                        # Парсим перечень тестов
                        for j, pm_block in enumerate(pm_blocks):
                            # Проверяем является ли строка заголовком и содержит ли нужный хештег
                            if re.search('h3', pm_block) or ((re.search('#all', pm_block) or re.search(tag, pm_block)) and re.search('\[', pm_block)):
                                if re.search('h3', pm_block):
                                    category = pm_blocks[j][4:-1]
                                else:
                                    tests.append(category)
                                    tests.append(pm_blocks[j][4:pm_blocks[j].find('|')])
                                    tests.append(pm_blocks[j][pm_blocks[j].find('|')+1:pm_blocks[j].find(']]')])
                i = 0
                while i < len(tests)/3:
                    category = tests[::3][i]
                    keyword = tests[1::3][i]
                    name = tests[2::3][i]
                    new_test = Test(testplan=TestPlan.objects.get(id=testplan_id), category=category,
                                    url='http://lab.server.group/projects/'+project_id+'/wiki/'+keyword+'/',
                                    name=name)
                    new_test.save()
                    i += 1
                # импортируем описание процедур и ожидаемых результатов
                tests = Test.objects.filter(testplan=testplan_id)
                for test in tests:
                    project_key = get_project_and_keyword_from_test(test.id)
                    test_details = parse_test_details_from_redmine(project_key[0], project_key[1], tag)
                    test.procedure = test_details[1]
                    test.expected = test_details[2]
                    test.save()
                return HttpResponseRedirect('/testplan/' + str(testplan_id) + '/')
            except ResourceNotFoundError:
                error = 'Проект не найден!'
                return render(request, 'testplan/testplan_import_error.html', {'error': error,
                                                                               'testplan_id': testplan_id})
    else:
        device_types = DeviceType.objects.filter(~Q(sub_type='')).order_by('sub_type')
        return render(request, 'testplan/testplan_import.html', {'device_types': device_types,
                                                                 'testplan_id': testplan_id})


def get_project_and_keyword_from_test(test_id):
    test = get_object_or_404(Test, id=test_id)
    split_url = test.url.split('/')
    project_id = split_url[4]
    keyword = split_url[6]
    return project_id, keyword


def parse_test_details_from_redmine(project_id, keyword, tag):
    name = procedure = expected = ''
    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.1.1')
    try:
        wiki_page = redmine.wiki_page.get(keyword.title(), project_id=project_id)
        blocks = wiki_page.text.split('h2. ')
        name = blocks[0][11:-4]
        for i, block in enumerate(blocks):
            parser = re.search('Процедура', block)
            if parser:
                procedure = blocks[i][13:-2]
        for i, block in enumerate(blocks):
            parser = re.search('Ожидаемый результат', block)
            if parser:
                expected = blocks[i][23::]
        return name, collapse_filter(procedure, tag), collapse_filter(expected, tag)
    except ResourceNotFoundError:
        return name, procedure, expected


def collapse_filter(ctx, tag):
    blocks = ctx.split('}}')
    for i, block in enumerate(blocks):
        if re.search('{{', block):
            if re.search('{{collapse\(', block):
                sblocks = block.split('{{collapse(')
                if re.search('__%{color:gray}#', sblocks[1]):
                    if re.search('#'+tag, sblocks[1]):
                        ssblocks = sblocks[1].split('%__')
                        blocks[i] = sblocks[0][:-2] + ssblocks[1][:-2]
                    else:
                        blocks[i] = sblocks[0][:-4]
                else:
                    s = sblocks[1].index(')')
                    trimmed_sblock = sblocks[1][:s] + sblocks[1][s + 1:]
                    sblocks[1] = trimmed_sblock[:-2]
                    blocks[i] = ''.join(sblocks)
            else:
                blocks[i] = blocks[i] + '}}'
    ctx = ''.join(blocks)
    return ctx
'''
