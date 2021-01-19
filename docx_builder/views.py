from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from protocol.models import Protocol
from django.utils.translation import gettext_lazy as _
from docx import Document
from django.conf import settings
import os
from django.http import HttpResponse, Http404
from django.utils.datastructures import MultiValueDictKeyError
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.text import WD_BREAK
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from .models import DocxProfile
from .forms import DocxProfileForm
from django.urls import reverse
from django.utils import timezone


@method_decorator(login_required, name='dispatch')
class DocxProfileListView(ListView):
    context_object_name = 'docx_profiles'
    queryset = DocxProfile.objects.all().order_by('id')
    template_name = 'docx_builder/docx_profiles.html'


@method_decorator(login_required, name='dispatch')
class DocxProfileCreate(CreateView):
    model = DocxProfile
    form_class = DocxProfileForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_profiles')
        return context

    def get_success_url(self):
        return reverse('docx_profiles')


@method_decorator(login_required, name='dispatch')
class DocxProfileUpdate(UpdateView):
    model = DocxProfile
    form_class = DocxProfileForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_profiles')
        return context

    def get_success_url(self):
        return reverse('docx_profiles')


@method_decorator(login_required, name='dispatch')
class DocxProfileDelete(DeleteView):
    model = DocxProfile
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('docx_profiles')
        return context

    def get_success_url(self):
        return reverse('docx_profiles')


@login_required
def build_protocol(request):
    if request.method == 'POST':
        protocol = get_object_or_404(Protocol, id=request.POST['protocol_id'])
        general = performance = results_table = summary = team = False
        try:
            if request.POST['general']:
                general = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['performance']:
                performance = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['results_table']:
                results_table = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['summary']:
                summary = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['team']:
                team = True
        except MultiValueDictKeyError:
            pass

        document = build_document()
        # margin
        section = document.sections
        section[0].left_margin = Cm(2)
        section[0].right_margin = Cm(1)
        section[0].top_margin = Cm(1)
        section[0].bottom_margin = Cm(1)
        ###
        if general:
            document.add_paragraph(str(_('General Information about DUT')), style='Heading 1')
            table = document.add_table(rows=0, cols=2)
            table.style = 'TableGrid'
            row_cells = table.add_row().cells
            row_cells[0].text = str(_('Device Type')) + ': '
            row_cells[1].text = protocol.device.type.name
            row_cells = table.add_row().cells
            row_cells[0].text = str(_('Vendor')) + ': '
            row_cells[1].text = protocol.device.vendor.name
            row_cells = table.add_row().cells
            row_cells[0].text = str(_('Model')) + ': '
            row_cells[1].text = protocol.device.model
            if protocol.device.hw:
                row_cells = table.add_row().cells
                row_cells[0].text = str(_('Hardware Version')) + ': '
                row_cells[1].text = protocol.device.hw
            row_cells = table.add_row().cells
            row_cells[0].text = str(_('Software Version')) + ': '
            row_cells[1].text = protocol.sw
            if protocol.sw_checksum:
                row_cells = table.add_row().cells
                row_cells[0].text = str(_('Software Checksum')) + ': '
                row_cells[1].text = protocol.sw_checksum
            row_cells = table.add_row().cells
            row_cells[0].merge(row_cells[1])
            row_cells[0].text = str(_('Hardware Specifications')) + ': '
            row_cells[0].paragraphs[0].runs[0].font.bold = True
            row_cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            if protocol.device.interfaces:
                row_cells = table.add_row().cells
                row_cells[0].text = str(_('Interfaces')) + ': '
                row_cells[1].text = protocol.device.interfaces
            if protocol.device.leds:
                row_cells = table.add_row().cells
                row_cells[0].text = str(_('Leds')) + ': '
                row_cells[1].text = protocol.device.leds
            if protocol.device.buttons:
                row_cells = table.add_row().cells
                row_cells[0].text = str(_('Buttons')) + ': '
                row_cells[1].text = protocol.device.buttons
            if protocol.device.chipsets:
                row_cells = table.add_row().cells
                row_cells[0].text = str(_('Chipsets')) + ': '
                row_cells[1].text = protocol.device.chipsets
            if protocol.device.memory:
                row_cells = table.add_row().cells
                row_cells[0].text = str(_('Memory')) + ': '
                row_cells[1].text = protocol.device.memory
            # cells width
            for cell in table.columns[0].cells:
                cell.width = Cm(4)
            for cell in table.columns[1].cells:
                cell.width = Cm(14.5)
            p = document.add_paragraph(str(_('Date of testing')) + ': ' +
                                       str(protocol.date_of_start.strftime("%d.%m.%Y")), style='Heading 2')
            if protocol.date_of_finish:
                p.add_run(' - ' + str(protocol.date_of_finish.strftime("%d.%m.%Y")))
            document.add_paragraph(str(_('Photo')), style='Heading 1')
            table = document.add_table(rows=0, cols=1)
            table.style = 'TableGrid'
            row_cells = table.add_row().cells
            row_cells[0].text = str('')

            p = document.add_paragraph()
            run = p.add_run()
            run.add_break(WD_BREAK.PAGE)

        if performance:
            document.add_paragraph(str(_('Performance results')), style='Heading 1')

            p = document.add_paragraph()
            run = p.add_run()
            run.add_break(WD_BREAK.PAGE)

        if results_table:
            results = protocol.get_results(headers=True)
            document.add_paragraph(str(_('Test results')), style='Heading 1')
            document.add_paragraph(str(_('Testing was carried out in accordance with testplan of ')) +
                                   protocol.testplan.name + ' (' + str(_('document version')) + ': ' +
                                   protocol.testplan.version + ').', style='Normal')
            p = document.add_paragraph(str(_('The table below shows the test results. Description of "Res." column: '
                                             )), style='Normal')
            run = p.add_run(u'\u2713')
            run.bold = True
            run.font.color.rgb = RGBColor(0x00, 0x80, 0x00)
            p.add_run(' - ' + str(_('Successful')) + ', ')
            run = p.add_run(u'\u274C')
            run.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
            p.add_run(' - ' + str(_('Failed')) + ', ')
            run = p.add_run('?')
            run.bold = True
            p.add_run(' - ' + str(_('Skipped')) + ', ')
            run = p.add_run(u'\u00b1')
            run.bold = True
            p.add_run(' - ' + str(_('Passed with warning')) + '.')

            table = document.add_table(rows=1, cols=4)
            table.style = 'TableGrid'
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = '№'
            hdr_cells[1].text = str(_('Test name'))
            hdr_cells[2].text = str(_('Res.'))
            hdr_cells[3].text = str(_('Comment'))
            for hdr_cell in hdr_cells:
                hdr_cell.paragraphs[0].runs[0].font.bold = True

            for result in results:
                row_cells = table.add_row().cells
                if result['header']:
                    row_cells[1].merge(row_cells[2]).merge(row_cells[3])
                    row_cells[0].text = str(result['num'])
                    row_cells[0].paragraphs[0].runs[0].font.bold = True
                    row_cells[1].text = str(result['category_name'])
                    row_cells[1].paragraphs[0].runs[0].font.bold = True
                else:
                    row_cells[0].text = str(result['num'][0]) + '.' + str(result['num'][1])
                    row_cells[1].text = str(result['test_name'])
                    paragraph = row_cells[2].paragraphs[0]
                    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    run = paragraph.add_run()
                    if result['result'] == 0 or result['result'] is None:
                        run.add_text('?')
                        run.font.bold = True
                    elif result['result'] == 1:
                        run.add_text(u'\u274C')
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
                    elif result['result'] == 2:
                        run.add_text(u'\u00b1')
                        run.font.bold = True
                    elif result['result'] == 3:
                        run.add_text(u'\u2713')
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(0x00, 0x80, 0x00)
                    row_cells[3].text = str(result['comment'])
            # cells width
            for cell in table.columns[0].cells:
                cell.width = Cm(1.4)
            for cell in table.columns[1].cells:
                cell.width = Cm(12.5)
            for cell in table.columns[2].cells:
                cell.width = Cm(1)
            for cell in table.columns[3].cells:
                cell.width = Cm(4)
            # page break
            p = document.add_paragraph()
            run = p.add_run()
            run.add_break(WD_BREAK.PAGE)

        if summary:
            issues = protocol.get_issues()
            document.add_paragraph(str(_('Protocol summary')), style='Heading 1')
            p = document.add_paragraph(str(_('During testing of device ')), style='Normal')
            run = p.add_run(protocol.device.model)
            run.bold = True
            p.add_run(str(_(' from manufacturer ')))
            run = p.add_run(protocol.device.vendor.name)
            run.bold = True
            p.add_run(str(_(' with firmware version ')))
            run = p.add_run(protocol.sw)
            run.bold = True
            p.add_run(str(_(' and hardware version ')))
            run = p.add_run(protocol.device.hw)
            run.bold = True
            if issues:
                p.add_run(str(_(', the following issues were found:')))
                for issue in issues:
                    document.add_paragraph(issue['text'], style='List Number')
            else:
                p.add_run(str(_(', issues not found.')))

        if team:
            document.add_paragraph(str(_('Worked on testing')), style='Heading 1')

        ###
        file = os.path.join(settings.MEDIA_ROOT + '/docx_builder/protocols/', 'Protocol_' + str(protocol.id) + '.docx')
        document.save(file)
        if os.path.exists(file):
            with open(file, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
                return response
        raise Http404

    else:
        message = [False, _('Page not found')]
        return render(request, 'device/message.html', {'message': message})


@login_required
def build_protocol_detailed(request):
    return Http404


def build_document():
    document = Document()
    document.styles['Heading 1'].font.name = 'Calibri'
    document.styles['Heading 1'].font.color.rgb = RGBColor(0x77, 0x00, 0xFF)
    document.styles['Heading 1'].font.size = Pt(16)
    document.styles['Heading 1'].font.bold = True
    document.styles['Heading 1'].font.italic = False
    document.styles['Heading 1'].font.underline = False
    document.styles['Heading 1'].paragraph_format.space_before = Pt(5)
    document.styles['Heading 1'].paragraph_format.space_after = Pt(5)

    document.styles['Heading 2'].font.name = 'Calibri'
    document.styles['Heading 2'].font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    document.styles['Heading 2'].font.size = Pt(12)
    document.styles['Heading 2'].font.bold = False
    document.styles['Heading 2'].font.italic = False
    document.styles['Heading 2'].font.underline = False
    document.styles['Heading 2'].paragraph_format.space_before = Pt(5)
    document.styles['Heading 2'].paragraph_format.space_after = Pt(5)
    return document
