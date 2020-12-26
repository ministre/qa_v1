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
from docx.shared import Cm


@login_required
def build_protocol_beta(request):
    if request.method == 'POST':
        protocol = get_object_or_404(Protocol, id=request.POST['protocol_id'])
        results_table = False
        try:
            if request.POST['results_table']:
                results_table = True
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
            document.add_paragraph('Test results', style='Heading 1')

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
    return document
