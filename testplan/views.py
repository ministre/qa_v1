from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from qa_v1 import settings
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
import re
from testplan.models import TestPlan, Test
from device.models import DeviceType
from django.http import HttpResponseRedirect
from .forms import TestPlanForm, TestForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse


@method_decorator(login_required, name='dispatch')
class TestplanListView(ListView):
    context_object_name = 'testplans'
    queryset = TestPlan.objects.all().order_by("-id")
    template_name = 'testplan/testplans.html'


@method_decorator(login_required, name='dispatch')
class TestplanCreate(CreateView):
    model = TestPlan
    form_class = TestPlanForm
    template_name = 'testplan/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('testplans')
        return context

    def get_success_url(self):
        return reverse('testplans')


@login_required
def testplan_details(request, pk):
    testplan = get_object_or_404(TestPlan, id=pk)
    tests = Test.objects.filter(testplan=testplan).order_by("id")
    numbers_of_tests = get_numbers_of_tests(tests)
    zipped_results = zip(tests, numbers_of_tests)
    return render(request, 'testplan/testplan_detail.html',
                  {'testplan_id': testplan.id,
                   'testplan': testplan,
                   'tests': zipped_results})


@login_required
def clear(request, testplan_id):
    Test.objects.filter(testplan=testplan_id).delete()
    return HttpResponseRedirect('/testplan/' + str(testplan_id) + '/')


@login_required
def test_delete(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    Test.objects.filter(id=test_id).delete()
    return HttpResponseRedirect('/testplan/' + str(test.testplan.id) + '/')


@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    tags = DeviceType.objects.filter(~Q(sub_type='')).order_by("sub_type")
    if request.method == "POST":
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            test = form.save(commit=False)
            test.save()
            return HttpResponseRedirect('/testplan/' + str(test.testplan.id) + '/')
    else:
        form = TestForm(instance=test)
    return render(request, 'testplan/test_detail.html', {'test': test, 'form': form,
                                                         'testplan': test.testplan.id,
                                                         'tags': tags})


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
def testplan_delete(request, testplan_id):
    TestPlan.objects.filter(id=testplan_id).delete()
    return HttpResponseRedirect('/testplan/')


@login_required
def testplan_edit(request, testplan_id):
    if request.method == 'POST':
        form = TestPlanForm(request.POST)
        if form.is_valid():
            testplan = TestPlan.objects.get(id=testplan_id)
            testplan.version = request.POST['version']
            testplan.name = request.POST['name']
            testplan.save()
            return HttpResponseRedirect('/testplan/')
    else:
        testplan = TestPlan.objects.get(id=testplan_id)
        form = TestPlanForm(initial={'version': testplan.version, 'name': testplan.name})
        return render(request, 'testplan/testplan_edit.html', {'form': form, 'testplan': testplan})


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
            redmine = Redmine(redmine_config.REDMINE_URL, username=redmine_config.REDMINE_USERNAME,
                              password=redmine_config.REDMINE_PASSWORD)
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
