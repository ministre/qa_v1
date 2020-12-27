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


@login_required
def build_protocol_beta(request):
    if request.method == 'POST':
        protocol = get_object_or_404(Protocol, id=request.POST['protocol_id'])
        results_table = summary = False
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

        document = build_document()
        # margin
        section = document.sections
        section[0].left_margin = Cm(2)
        section[0].right_margin = Cm(1)
        section[0].top_margin = Cm(1)
        section[0].bottom_margin = Cm(1)
        ###
        if results_table:
            results = protocol.get_results(headers=True)
            document.add_paragraph('Test results', style='Heading 1')
            document.add_paragraph(str(_('Testing was carried out in accordance with testplan of ')) +
                                   protocol.testplan.name + ' (' + str(_('document version')) + ': ' +
                                   protocol.testplan.version + ').', style='Normal')
            p = document.add_paragraph(str(_('The table below shows the test results. Description of "Res." column: '
                                             )), style='Normal')
            run = p.add_run(u'\u2713')
            run.bold = True
            run.font.color.rgb = RGBColor(0x00, 0x80, 0x00)
            p.add_run(' - ' + str(_('successful')) + ', ')
            run = p.add_run(u'\u274C')
            run.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
            p.add_run(' - ' + str(_('failed')) + ', ')
            run = p.add_run('?')
            run.bold = True
            p.add_run(' - ' + str(_('skipped')) + ', ')
            run = p.add_run(u'\u00b1')
            run.bold = True
            p.add_run(' - ' + str(_('passed with warning')) + '.')

            table = document.add_table(rows=1, cols=4)
            table.style = 'TableGrid'
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = '№'
            hdr_cells[1].text = str(_('Names'))
            hdr_cells[2].text = str(_('Res.'))
            hdr_cells[3].text = str(_('Comments'))
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
            document.add_paragraph('Summary', style='Heading 1')
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

    return document
