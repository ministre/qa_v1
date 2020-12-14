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
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404


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


@method_decorator(login_required, name='dispatch')
class DocxTemplateFileDelete(DeleteView):
    model = DocxTemplateFile
    template_name = 'docx_generator/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_template_update', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('docx_templates')


@login_required
def build_protocol(request):
    if request.method == "POST":
        protocol = get_object_or_404(Protocol, id=request.POST['protocol_id'])
        docx_template = get_object_or_404(DocxTemplateFile, id=request.POST['docx_template_id'])
        tests = comments = []
        results = TestResult.objects.filter(protocol=protocol).order_by("id")
        zipped_results = zip(results, get_numbers_of_results(results))
        status = None
        for result, num in zipped_results:
            if result.result == 0:
                status = RichText('Пропущен', color='black')
            elif result.result == 1:
                status = RichText('X', color='red', bold=True)
            elif result.result == 2:
                status = RichText(u'\u00b1', color='black', bold=True)
            elif result.result == 3:
                status = RichText(u'\u221a', color='green', bold=True)
            test = {'num': num, 'name': result.test.name, 'status': status, 'comment': Listing(result.comment)}
            tests.append(test)
            if result.comment != '' and result.comment != ' ':
                comment = {'text': Listing(result.comment)}
                comments.append(comment)
        protocol_file = DocxTemplate(docx_template.file)
        context = {'testplan': protocol.testplan.name,
                   'vendor': protocol.device.vendor,
                   'model': protocol.device.model,
                   'hw': protocol.device.hw,
                   'sw': protocol.sw,
                   'checksum': protocol.sw_checksum,
                   'interfaces': protocol.device.interfaces,
                   'leds': protocol.device.leds,
                   'buttons': protocol.device.buttons,
                   'chipsets': protocol.device.chipsets,
                   'memory': protocol.device.memory,
                   'started': localize(protocol.date_of_start),
                   'completed': localize(protocol.date_of_finish),
                   'version': protocol.testplan.version,
                   'tests': tests,
                   'comments': comments
                   }
        protocol_file.render(context)
        file = os.path.join(settings.MEDIA_ROOT + '/docx_generator/protocols/',
                            'Protocol_' + str(protocol.id) + '.docx')
        protocol_file.save(file)
        if os.path.exists(file):
            with open(file, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
                return response
        raise Http404
    else:
        message = [False, _('Page not found')]
        return render(request, 'docx_generator/message.html', {'message': message})


@login_required
def build_protocol_detailed(request):
    if request.method == "POST":
        protocol = get_object_or_404(Protocol, id=request.POST['protocol_id'])
        docx_template = get_object_or_404(DocxTemplateFile, id=request.POST['docx_template_id'])
        vendor = protocol.device.vendor
        model = protocol.device.model
        hw = protocol.device.hw
        sw = protocol.sw
        results = TestResult.objects.filter(protocol=protocol).order_by("id")
        protocol_detailed_file = DocxTemplate(docx_template.file)
        results_table = []
        for result in results:
            result_string = {'category': result.test.category, 'name': result.test.name,
                             'config': Listing(result.config), 'info': Listing(result.info)}
            results_table.append(result_string)
        context = {'vendor': vendor, 'model': model, 'hw': hw, 'sw': sw, 'tests': results_table}
        protocol_detailed_file.render(context)
        file = os.path.join(settings.MEDIA_ROOT + '/docx_generator/protocols_detailed/',
                            'ProtocolDetailed_' + str(protocol.id) + '.docx')
        protocol_detailed_file.save(file)
        if os.path.exists(file):
            with open(file, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
                return response
        raise Http404
    else:
        message = [False, _('Page not found')]
        return render(request, 'docx_generator/message.html', {'message': message})


@login_required
def build_testplan(request):
    if request.method == "POST":
        testplan = get_object_or_404(TestPlan, id=request.POST['testplan_id'])
        docx_template = get_object_or_404(DocxTemplateFile, id=request.POST['docx_template_id'])
        tests_table = []
        tests = Test.objects.filter(testplan=testplan).order_by("id")
        for test in tests:
            test_string = {'category': test.category, 'name': test.name, 'procedure': Listing(test.procedure),
                           'expected': Listing(test.expected)}
            tests_table.append(test_string)
        testplan_file = DocxTemplate(docx_template.file)
        context = {'testplan': testplan.name, 'version': testplan.version, 'tests': tests_table}
        testplan_file.render(context)
        file = os.path.join(settings.MEDIA_ROOT + '/docx_generator/testplans/',
                            'Testplan_' + str(testplan.id) + '.docx')
        testplan_file.save(file)
        if os.path.exists(file):
            with open(file, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
                return response
        raise Http404
    else:
        message = [False, _('Page not found')]
        return render(request, 'docx_generator/message.html', {'message': message})
