from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from device.models import Device
from testplan.models import TestPlan, Test
from .models import Protocol, TestResult, TestResultNote, TestResultConfig, TestResultImage, TestResultFile, \
    TestResultIssue
from django.http import HttpResponseRedirect
from .forms import ProtocolForm, ResultForm, ResultNoteForm, ResultConfigForm, ResultImageForm, ResultIssueForm, \
    ResultFileForm, ProtocolCopyResultsForm
from redmine.forms import RedmineProtocolExportForm, RedmineResultExportForm
from docx_builder.forms import BuildDocxProtocolForm
from docx_generator.forms import BuildProtocolForm, BuildProtocolDetailedForm
from qa_v1 import settings
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
import re
from django.db.models import Q
import textile
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from device.views import Item


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

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user, 'date_of_start': datetime.now()}

    def get_form(self, form_class=ProtocolForm):
        form = super(ProtocolCreate, self).get_form(form_class)
        form.fields['redmine_wiki'].widget = forms.HiddenInput()
        form.fields['result'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('protocols')
        return context

    def get_success_url(self):
        self.object.redmine_wiki = 'Protocol_' + str(self.object.id)
        self.object.save()
        return reverse('protocols')


@method_decorator(login_required, name='dispatch')
class ProtocolUpdate(UpdateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

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
    protocol = get_object_or_404(Protocol, id=pk)
    results = TestResult.objects.filter(protocol=pk).order_by("id")

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

    build_protocol_form = BuildDocxProtocolForm(initial={'protocol_id': protocol.id})
    protocol_form = BuildProtocolForm(initial={'protocol_id': protocol.id})

    protocol_form.fields['protocol_id'].widget = forms.HiddenInput()
    protocol_detailed_form = BuildProtocolDetailedForm(initial={'protocol_id': protocol.id})
    protocol_detailed_form.fields['protocol_id'].widget = forms.HiddenInput()
    copy_test_results_form = ProtocolCopyResultsForm(device_id=protocol.device.id, dst_protocol=protocol.id)

    export_form = RedmineProtocolExportForm(initial={'protocol_id': protocol.id,
                                                     'redmine_project': protocol.device.redmine_project,
                                                     'redmine_wiki': protocol.redmine_wiki,
                                                     'general': True, 'results': True})
    results = protocol.get_results()
    return render(request, 'protocol/protocol_details.html', {'protocol': protocol,
                                                              'results': results,
                                                              'tests_all': tests_all,
                                                              'tests_completed': tests_completed,
                                                              'tests_completed_percent': tests_completed_percent,
                                                              'tests_left': tests_left,
                                                              'tests_success': tests_success,
                                                              'tests_warn': tests_warn,
                                                              'tests_fail': tests_fail,
                                                              'build_protocol_form': protocol_form,
                                                              'build_protocol_form_beta': build_protocol_form,
                                                              'build_protocol_detailed_form': protocol_detailed_form,
                                                              'copy_test_results_form': copy_test_results_form,
                                                              'redmine_url': settings.REDMINE_URL,
                                                              'export_form': export_form,
                                                              'tab_id': tab_id})


@login_required
def result_create(request, protocol_id: int, test_id: int):
    protocol = get_object_or_404(Protocol, id=protocol_id)
    test = get_object_or_404(Test, id=test_id)
    num = test.get_num()
    if test.redmine_wiki:
        redmine_wiki = str(num[0]) + '_' + str(num[1]) + '_' + test.redmine_wiki + '_'
    else:
        redmine_wiki = str(num[0]) + '_' + str(num[1]) + '_'
    result, create = TestResult.objects.update_or_create(protocol=protocol, test=test,
                                                         defaults={'created_by': request.user,
                                                                   'updated_by': request.user})
    redmine_wiki += str(result.id)
    result.redmine_wiki = redmine_wiki
    result.save()
    return HttpResponseRedirect(reverse('result_details', kwargs={'pk': result.id, 'tab_id': 7}))


@method_decorator(login_required, name='dispatch')
class ResultUpdate(UpdateView):
    model = TestResult
    form_class = ResultForm
    template_name = 'protocol/update.html'

    def get_form(self, form_class=ResultForm):
        form = super(ResultUpdate, self).get_form(form_class)
        form.fields['result'].widget = forms.HiddenInput()
        form.fields['comment'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('result_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class ResultDelete(DeleteView):
    model = TestResult
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.protocol, user=self.request.user)
        return reverse('protocol_details', kwargs={'pk': self.object.protocol.id, 'tab_id': 2})


@login_required
def result_details(request, pk, tab_id):
    result = get_object_or_404(TestResult, id=pk)
    if request.method == "POST":
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            test = form.save(commit=False)
            test.updated_at = timezone.now()
            test.updated_by = request.user
            test.save()
            return HttpResponseRedirect(reverse('protocol_details', kwargs={'pk': result.protocol.id, 'tab_id': 2}))
    else:
        procedure = textile.textile(result.test.procedure)
        expected = textile.textile(result.test.expected)
        num = result.test.get_num()
        result_form = ResultForm(instance=result)
        result_form.fields['redmine_wiki'].widget = forms.HiddenInput()
        export_form = RedmineResultExportForm(initial={'result_id': result.id,
                                                       'redmine_project': result.protocol.device.redmine_project,
                                                       'redmine_wiki': result.redmine_wiki,
                                                       'redmine_parent_wiki': result.protocol.redmine_wiki})

        return render(request, 'protocol/result_details.html', {'result': result, 'procedure': procedure,
                                                                'expected': expected, 'num': num,
                                                                'result_form': result_form,
                                                                'export_form': export_form,
                                                                'redmine_url': settings.REDMINE_URL, 'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class ResultNoteCreate(CreateView):
    model = TestResultNote
    form_class = ResultNoteForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'result': self.kwargs.get('result'), 'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.kwargs.get('result'), 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class ResultNoteUpdate(UpdateView):
    model = TestResultNote
    form_class = ResultNoteForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class ResultNoteDelete(DeleteView):
    model = TestResultNote
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class ResultConfigCreate(CreateView):
    model = TestResultConfig
    form_class = ResultConfigForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'result': self.kwargs.get('result'), 'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.kwargs.get('result'), 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class ResultConfigUpdate(UpdateView):
    model = TestResultConfig
    form_class = ResultConfigForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class ResultConfigDelete(DeleteView):
    model = TestResultConfig
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class ResultImageCreate(CreateView):
    model = TestResultImage
    form_class = ResultImageForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'result': self.kwargs.get('result'), 'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.kwargs.get('result'), 'tab_id': 5})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class ResultImageUpdate(UpdateView):
    model = TestResultImage
    form_class = ResultImageForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class ResultImageDelete(DeleteView):
    model = TestResultImage
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class ResultFileCreate(CreateView):
    model = TestResultFile
    form_class = ResultFileForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'result': self.kwargs.get('result'), 'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.kwargs.get('result'), 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class ResultFileUpdate(UpdateView):
    model = TestResultFile
    form_class = ResultFileForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class ResultFileDelete(DeleteView):
    model = TestResultFile
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class ResultIssueCreate(CreateView):
    model = TestResultIssue
    form_class = ResultIssueForm
    template_name = 'protocol/create.html'

    def get_initial(self):
        return {'result': self.kwargs.get('result'), 'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.kwargs.get('result'), 'tab_id': 7})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class ResultIssueUpdate(UpdateView):
    model = TestResultIssue
    form_class = ResultIssueForm
    template_name = 'protocol/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class ResultIssueDelete(DeleteView):
    model = TestResultIssue
    template_name = 'protocol/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        Item.update_timestamp(foo=self.object.result, user=self.request.user)
        return reverse('result_details', kwargs={'pk': self.object.result.id, 'tab_id': 7})


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
    else:
        devices = Device.objects.all()
        return render(request, 'protocol/protocol_import.html', {'devices': devices})


@login_required
def protocol_copy_results(request):
    if request.method == 'POST':
        src_protocol = get_object_or_404(Protocol, id=request.POST['src_protocol'])
        dst_protocol = get_object_or_404(Protocol, id=request.POST['dst_protocol'])
        dst_results = TestResult.objects.filter(protocol=dst_protocol)
        for dst_result in dst_results:
            src_results = TestResult.objects.filter(protocol=src_protocol)
            for src_result in src_results:
                if src_result.test.name == dst_result.test.name:
                    dst_result.result = src_result.result
                    dst_result.config = src_result.config
                    dst_result.info = src_result.info
                    dst_result.comment = src_result.comment
                    dst_result.save()
        return HttpResponseRedirect(reverse('protocol_details', kwargs={'pk': dst_protocol.id, 'tab_id': 2}))
    else:
        message = [False, _('Page not found')]
        return render(request, 'docx_generator/message.html', {'message': message})
