from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DocxTemplateFileForm
from docx_generator.models import DocxTemplateFile
from docxtpl import DocxTemplate, RichText, Listing
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from protocol.models import Protocol, TestResult
from testplan.models import TestPlan, Test
from protocol.views import get_numbers_of_results
from django.utils.formats import localize
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse


@method_decorator(login_required, name='dispatch')
class DocxTemplateFileListView(ListView):
    context_object_name = 'docx_templates'
    queryset = DocxTemplateFile.objects.all().order_by("-id")
    template_name = 'docx_generator/docx_templates.html'


@method_decorator(login_required, name='dispatch')
class DocxTemplateFileCreate(CreateView):
    model = DocxTemplateFile
    form_class = DocxTemplateFileForm
    template_name = 'docx_generator/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_templates')
        return context

    def get_success_url(self):
        return reverse('docx_templates')


@method_decorator(login_required, name='dispatch')
class DocxTemplateFileUpdate(UpdateView):
    model = DocxTemplateFile
    form_class = DocxTemplateFileForm
    template_name = 'docx_generator/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_templates')
        return context

    def get_success_url(self):
        return reverse('docx_templates')


@login_required
def template_delete(request, template_id):
    DocxTemplateFile.objects.filter(id=template_id).delete()
    return HttpResponseRedirect('/docx/')


@login_required
def create_docx_detailed_protocol(request, pk):
    # собираем исходные данные
    protocol = Protocol.objects.get(id=pk)
    # перменные шаблона
    testplan = protocol.testplan.name
    vendor = protocol.device.vendor
    model = protocol.device.model
    hw = protocol.device.hw
    sw = protocol.sw
    results = TestResult.objects.filter(protocol=pk).order_by("id")
    protocol_file = DocxTemplate("docx_templates/detailed_protocol_switches.docx")
    results_table = []
    for result in results:
        result_string = {'category': result.test.category, 'name': result.test.name,
                         'config': Listing(result.config), 'info': Listing(result.info)}
        results_table.append(result_string)
    context = {'vendor': vendor, 'model': model, 'hw': hw, 'sw': sw, 'tests': results_table}

    protocol_file.render(context)
#    protocol_filename = 'docx_protocols/detailed_protocol_' + str(protocol.id) + '.docx'
    protocol_filename = 'Detailed_protocol_' + str(protocol.id) + '.docx'
#    protocol_file.save(protocol_filename)
    protocol_file.save(settings.MEDIA_ROOT + '/docx_generator/' + protocol_filename)
    # возвращаем протокол
#    file_path = os.path.join(settings.MEDIA_ROOT, protocol_filename)
    file_path = os.path.join(settings.MEDIA_ROOT + '/docx_generator/', protocol_filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required
def create_docx_protocol(request, pk):
    # собираем исходные данные
    protocol = Protocol.objects.get(id=pk)
    # перменные шаблона
    testplan = protocol.testplan.name
    vendor = protocol.device.vendor
    model = protocol.device.model
    hw = protocol.device.hw
    sw = protocol.sw
    sw_checksum = protocol.sw_checksum
    interfaces = protocol.device.interfaces
    leds = protocol.device.leds
    buttons = protocol.device.buttons
    chipsets = protocol.device.chipsets
    memory = protocol.device.memory
    date_of_start = localize(protocol.date_of_start)
    date_of_finish = localize(protocol.date_of_finish)
    date_of_file = str(protocol.date_of_finish)
    version = protocol.testplan.version

    # таблица с результатами
    results_table = []
    summary_comments = []
    results = TestResult.objects.filter(protocol=pk).order_by("id")
    numbers_of_testplan = get_numbers_of_results(results)
    zipped_results = zip(results, numbers_of_testplan)
    result_status = 'null'
    for result, num in zipped_results:
        if result.result == 0:
            result_status = RichText('Пропущен', color='black')
        if result.result == 1:
            result_status = RichText('X', color='red', bold=True)
        if result.result == 2:
            result_status = RichText(u'\u00b1', color='black', bold=True)
        if result.result == 3:
            result_status = RichText(u'\u221a', color='green', bold=True)
        result_string = {'num': num, 'testname': result.test.name, 'testresult': result_status,
                         'testcomment': Listing(result.comment)}
        results_table.append(result_string)
        if result.comment != '':
            summary_comment_string = {'text': Listing(result.comment)}
            summary_comments.append(summary_comment_string)

    # генерируем протокол
    # if protocol.device.type.id != 3:
    protocol_file = DocxTemplate("docx_templates/protocol_sw_acc.docx")
    # else:
    #    protocol_file = DocxTemplate("docx_templates/protocol_switches.docx")

    context = {'testplan': testplan, 'vendor': vendor, 'model': model, 'hw': hw, 'sw': sw, 'sw_checksum': sw_checksum,
               'interfaces': interfaces, 'leds': leds, 'buttons': buttons, 'chipsets': chipsets, 'memory': memory,
               'date_of_start': date_of_start, 'date_of_finish': date_of_finish, 'version': version,
               'tbl_contents': results_table,
               'comments': summary_comments
               }
    protocol_file.render(context)
    #protocol_filename = 'docx_protocols/Protocol_' + str(protocol.id) + '_' + date_of_file + '.docx'
    protocol_filename = 'Protocol_' + str(protocol.id) + '_' + date_of_file + '.docx'
    protocol_file.save(settings.MEDIA_ROOT + '/docx_generator/' + protocol_filename)
    # возвращаем протокол
    file_path = os.path.join(settings.MEDIA_ROOT + '/docx_generator/', protocol_filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required
def create_docx_testplan(request, testplan_id):
    # собираем исходные данные
    testplan = TestPlan.objects.get(id=testplan_id)

    tests_table = []
    tests = Test.objects.filter(testplan=testplan_id).order_by("id")
    for test in tests:
        test_string = {'category': test.category, 'name': test.name, 'procedure': Listing(test.procedure),
                       'expected': Listing(test.expected)}
        tests_table.append(test_string)

    # генерируем ПМИ
    testplan_file = DocxTemplate("docx_templates/testplan_cpe.docx")

    context = {'testplan': testplan.name, 'version': testplan.version, 'tests': tests_table}
    testplan_file.render(context)
#    testplan_filename = 'docx_testplans/Testplan_' + str(testplan_id) + '.docx'
    testplan_filename = 'Testplan_' + str(testplan_id) + '.docx'
#    testplan_file.save(testplan_filename)
    testplan_file.save(settings.MEDIA_ROOT + '/docx_generator/' + testplan_filename)
    # возвращаем ПМИ
#    file_path = os.path.join(settings.MEDIA_ROOT, testplan_filename)
    file_path = os.path.join(settings.MEDIA_ROOT + '/docx_generator/', testplan_filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
