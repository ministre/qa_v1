from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from device.models import Device
from testplan.models import TestPlan, Test
from protocol.models import Protocol, TestResult
from django.http import HttpResponseRedirect
from .forms import ProtocolForm, TestResultForm
from docx_generator.forms import BuildProtocolForm, BuildProtocolDetailedForm
from qa_v1 import settings
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
import re
from datetime import datetime
from django.db.models import Q
import textile
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django import forms


@method_decorator(login_required, name='dispatch')
class ProtocolListView(ListView):
    context_object_name = 'protocols'
    queryset = Protocol.objects.all().order_by("-id")
    template_name = 'protocol/protocols.html'


@method_decorator(login_required, name='dispatch')
class ProtocolCreate(CreateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocols')
        return context

    def get_success_url(self):
        tests = Test.objects.filter(testplan=self.object.testplan).order_by("id")
        for test in tests:
            test_results = TestResult(test=test, protocol=self.object, result=0)
            test_results.save()
        return reverse('protocols')


@method_decorator(login_required, name='dispatch')
class ProtocolUpdate(UpdateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/update.html'

    def get_form(self, form_class=ProtocolForm):
        form = super(ProtocolUpdate, self).get_form(form_class)
        form.fields['device'].widget = forms.HiddenInput()
        form.fields['testplan'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('protocol_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class ProtocolDelete(DeleteView):
    model = Protocol
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('protocols')


@login_required
def protocol_details(request, pk, tab_id):
    protocol = Protocol.objects.get(id=pk)
    results = TestResult.objects.filter(protocol=pk).order_by("id")

    numbers_of_testplan = get_numbers_of_results(results)
    zipped_results = zip(results, numbers_of_testplan)

    tests_all = results.count()
    tests_completed = TestResult.objects.filter(Q(protocol=pk) & ~Q(result=0)).count()
    if tests_all > 0:
        tests_completed_percent = round(tests_completed * 100 / tests_all, 1)
    else:
        tests_completed_percent = 0
    tests_left = tests_all - tests_completed
    tests_success = TestResult.objects.filter(Q(protocol=pk) & Q(result=3)).count()
    tests_warn = TestResult.objects.filter(Q(protocol=pk) & Q(result=2)).count()
    tests_fail = TestResult.objects.filter(Q(protocol=pk) & Q(result=1)).count()

    protocol_form = BuildProtocolForm(initial={'protocol_id': protocol.id})
    protocol_form.fields['protocol_id'].widget = forms.HiddenInput()
    protocol_detailed_form = BuildProtocolDetailedForm(initial={'protocol_id': protocol.id})
    protocol_detailed_form.fields['protocol_id'].widget = forms.HiddenInput()

    return render(request, 'protocol/protocol_details.html', {'protocol': protocol,
                                                              'zipped_results': zipped_results,
                                                              'tests_all': tests_all,
                                                              'tests_completed': tests_completed,
                                                              'tests_completed_percent': tests_completed_percent,
                                                              'tests_left': tests_left,
                                                              'tests_success': tests_success,
                                                              'tests_warn': tests_warn,
                                                              'tests_fail': tests_fail,
                                                              'build_protocol_form': protocol_form,
                                                              'build_protocol_detailed_form': protocol_detailed_form,
                                                              'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class TestResultUpdate(UpdateView):
    model = TestResult
    form_class = TestResultForm
    template_name = 'protocol/update_test_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})

        context['procedure'] = textile.textile(self.object.test.procedure)
        context['expected'] = textile.textile(self.object.test.expected)

        return context

    def get_success_url(self):
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})


@login_required
def protocol_export(request, pk):
    protocol = Protocol.objects.get(id=pk)
    project_id = protocol.device.project_id

    if protocol.sysinfo != "":
        if ('.jpg' in protocol.sysinfo) or ('.png' in protocol.sysinfo):
            protocol.sysinfo = '!' + protocol.sysinfo + '!'
        else:
            protocol.sysinfo = '<pre>' + protocol.sysinfo + '</pre>'
        protocol.sysinfo = '\n{{collapse(Системная информация)\n' + protocol.sysinfo + '\n}}\n'

    if protocol.console != "":
        protocol.console = '\n{{collapse(Параметры консольного порта)\n<pre>' + protocol.console + '</pre>\n}}'

    if protocol.sw_checksum != "":
        protocol.sw_checksum = ' |\n| Контрольная сумма ПО: | ' + protocol.sw_checksum + ' |\n'

    new_content = '| Версия ПО: | ' + protocol.sw + ' |\n' + protocol.sw_checksum + \
                  '| Дата тестирования: | ' + protocol.date_of_start.strftime('%d.%m.%Y') + ' - ' + \
                  protocol.date_of_finish.strftime('%d.%m.%Y') + \
                  ' |\n| Инженерный логин: | ' + protocol.engineer_login + ' |\n' \
                  '| Инженерный пароль: | ' + protocol.engineer_password + ' |\n' + protocol.sysinfo + \
                  protocol.console + '\n_Тестирование проведено в соответствии с ПМИ ' + \
                  protocol.testplan.name + ' (Редакция: ' + protocol.testplan.version + ')_\n\n' \
                  '|_. № |_. Название теста: |_. Результат: |_. Инфо: |_. Комментарии: |\n'

    results = TestResult.objects.filter(protocol=pk).order_by("id")

    numbers_of_testplan = get_numbers_of_results(results)
    zipped_results = zip(results, numbers_of_testplan)

    for result, num in zipped_results:
        test_status = 'null'
        if result.result == 0:
            test_status = '{{checkbox(?)}}'
        if result.result == 1:
            test_status = '{{checkbox(0)}}'
        if result.result == 2:
            test_status = u'\u00b1'
        if result.result == 3:
            test_status = '{{checkbox(1)}}'
        # вставляем заголовок
        digit = num.split('.')
        if digit[1] == '1':
            header = '|_. ' + digit[0] + ' |' + '\\4. *' + result.test.category + '* |\n'
        else:
            header = ''
        # конфиг и доп.сведения
        url = result.test.url
        keyword = url.split('/')
        cfg = '[[cfg_' + keyword[6] + '|конфиг]], '
        info = '[[res_' + keyword[6] + '|детали]]'
        # формируем строку теста
        result_string = header + '| ' + num + ' | "' + result.test.name + '":' + result.test.url + ' |_. ' + \
                        test_status + ' | ' + cfg + ' ' + info + '| ' + result.comment + ' |\n'
        new_content = new_content + result_string

    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.1.1')
    wiki_pages = redmine.wiki_page.filter(project_id=project_id)
    for page in wiki_pages:
        if page.title == 'Wiki':
            blocks = page.text.split('h2. ')
            for i, block in enumerate(blocks):
                parser = re.search('Результаты испытаний', block)
                if parser:
                    blocks[i] = 'Результаты испытаний \n\n' + new_content + '\n\n'
            new_wiki_page = 'h2. '.join(blocks)
            # обновление Wiki-страницы устройства
            redmine.wiki_page.update('Wiki', project_id=project_id, text=new_wiki_page)
    return HttpResponseRedirect('/protocol/' + str(pk) + '/')


@login_required
def protocol_import(request):
    if request.method == 'POST':
        device = Device.objects.get(id=request.POST['device_id'])
        redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.1.1')
        wiki_page = redmine.wiki_page.get('Wiki', project_id=device.project_id)
        blocks = wiki_page.text.split('h2. ')
        sw = ''
        sw_checksum = ''
        sysinfo = ''
        console = ''
        engineer_login = ''
        engineer_password = ''
        testplan_name = ''
        testplan_version = ''
        date_of_start = ''
        date_of_finish = ''
        for i, block in enumerate(blocks):
            parser = re.search('Результаты испытаний', block)
            if parser:
                results_blocks = blocks[i].split('|')
                for j, results_block in enumerate(results_blocks):
                    parser = re.search('Версия ПО:', results_block)
                    if parser:
                        sw = results_blocks[j + 1][1:-1]
                for j, results_block in enumerate(results_blocks):
                    parser = re.search('Контрольная сумма ПО:', results_block)
                    if parser:
                        sw_checksum = results_blocks[j + 1][1:-1]
                for j, results_block in enumerate(results_blocks):
                    parser = re.search('Дата тестирования:', results_block)
                    if parser:
                        date_of_test = results_blocks[j + 1].split('-')
                        date_of_start = datetime.strptime(date_of_test[0][1:-1], '%d.%m.%Y')
                        date_of_finish = datetime.strptime(date_of_test[1][1:-1], '%d.%m.%Y')
                for j, results_block in enumerate(results_blocks):
                    parser = re.search('Инженерный логин:', results_block)
                    if parser:
                        engineer_login = results_blocks[j + 1][1:-1]
                for j, results_block in enumerate(results_blocks):
                    parser = re.search('Инженерный пароль:', results_block)
                    if parser:
                        engineer_password = results_blocks[j + 1][1:-1]
                for j, results_block in enumerate(results_blocks):
                    parser = re.search('Системная информация', results_block)
                    if parser:
                        sysinfo_blocks = results_blocks[j].split('}}')
                        sysinfo = sysinfo_blocks[0][40:-7]
                for j, results_block in enumerate(results_blocks):
                    parser = re.search('Параметры консольного порта', results_block)
                    if parser:
                        console_blocks = results_blocks[j].split('}}')
                        console = console_blocks[1][47:-7]
                testplan_blocks = blocks[i].split('_')
                for j, testplan_block in enumerate(testplan_blocks):
                    parser = re.search('Тестирование проведено в соответствии с ПМИ', testplan_block)
                    if parser:
                        testplan_string = testplan_blocks[j].split('(Редакция:')
                        testplan_name = testplan_string[0][44:-1]
                        testplan_version = testplan_string[1][1:-1]
        # ищем ПМИ по названию и редакции
        testplan = TestPlan.objects.get(Q(name=testplan_name) & Q(version=testplan_version))
        # создаем протокол
        new_protocol = Protocol(device=device, testplan=testplan, sw=sw, sw_checksum=sw_checksum,
                                engineer_login=engineer_login, engineer_password=engineer_password,
                                sysinfo=sysinfo, console=console, date_of_start=date_of_start,
                                date_of_finish=date_of_finish)
        new_protocol.save()
        # создаем результаты тестов к протоколу
        for test in Test.objects.filter(testplan=testplan.id).order_by("id"):
            test_results = TestResult(test=test, protocol=new_protocol, result=0)
            test_results.save()
        # парсим результаты
        blocks = blocks[3].split('|')
        for i, block in enumerate(blocks):
            parser = re.search('/projects/', block)
            if parser:
                url_blocks = blocks[i].split('"')
                url = url_blocks[2][1:-1]
                result = blocks[i+1][3:-1]
                if result == '{{checkbox(?)}}' or '':
                    result = 0
                if result == '{{checkbox(0)}}':
                    result = 1
                if result == u'\u00b1':
                    result = 2
                if result == '{{checkbox(1)}}':
                    result = 3
                comment = blocks[i+5][1:-1]
                test = Test.objects.get(Q(url=url) & Q(testplan=testplan))
                test_result = TestResult.objects.get(Q(test=test.id) & Q(protocol=new_protocol))
                test_result.result = result
                test_result.comment = comment
                # парсим конфиг и детали теста
                wiki_cfg_url = 'Cfg_' + url.split('/')[6]
                wiki_info_url = 'Res_' + url.split('/')[6]
                try:
                    wiki_page = redmine.wiki_page.get(wiki_cfg_url, project_id=device.project_id)
                    test_result.config = wiki_page.text[5:-6]
                except ResourceNotFoundError:
                    test_result.config = ''
                try:
                    wiki_page = redmine.wiki_page.get(wiki_info_url, project_id=device.project_id)
                    test_result.info = wiki_page.text
                except ResourceNotFoundError:
                    test_result.info = ''
                test_result.save()
        # context = wiki_cfg_url
        return HttpResponseRedirect('/protocol/')
        # return render(request, 'protocol/debug.html', {'context': context})
    else:
        devices = Device.objects.all()
        return render(request, 'protocol/protocol_import.html', {'devices': devices})


@login_required
def protocol_inherit(request, protocol_id):
    if request.method == 'POST':
        src_protocol = request.POST['src_protocol']
        dst_results = TestResult.objects.filter(protocol=protocol_id)
        for dst_result in dst_results:
            src_results = TestResult.objects.filter(protocol=src_protocol)
            for src_result in src_results:
                if src_result.test.name == dst_result.test.name:
                    dst_result.result = src_result.result
                    dst_result.config = src_result.config
                    dst_result.info = src_result.info
                    dst_result.comment = src_result.comment
                    dst_result.save()
        return HttpResponseRedirect('/protocol/' + str(protocol_id) + '/')
    else:
        protocol = Protocol.objects.get(id=protocol_id)
        device = protocol.device.id
        protocol = Protocol.objects.filter(Q(device=device) & ~Q(id=protocol_id))
        if protocol:
            return render(request, 'protocol/protocol_inherit.html', {'protocol_id': protocol_id,
                                                                      'protocols': protocol})
        else:
            message = 'Нет других протоколов испытаний для данного оборудования!'
            return render(request, 'protocol/protocol_inherit_error.html', {'message': message})


def get_numbers_of_results(results):
    # генерируем нумерованный список тестов
    numbers_of_testplan = []
    category = None
    i = 0
    j = 0
    for res in results:
        new_category = res.test.category
        if new_category == category:
            j = j + 1
            numbers_of_testplan.append(str(i) + '.' + str(j))
        else:
            i = i + 1
            j = 1
            numbers_of_testplan.append(str(i) + '.' + str(j))
            category = res.test.category
    return numbers_of_testplan
