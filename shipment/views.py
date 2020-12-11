from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from qa_v1 import settings
from redminelib import Redmine
from docxtpl import DocxTemplate
import os
from django.http import HttpResponse, Http404
from django.conf import settings


@login_required
def shipment_list(request):
    redmine = Redmine(settings.HQ_REDMINE_URL, username=settings.HQ_REDMINE_USERNAME,
                      password=settings.HQ_REDMINE_PASSWORD)
    issues = redmine.issue.filter(project_id='controlc', status_id=9)
    vendors = []
    models = []
    orders = []
    contracts = []
    id = []
    for issue in issues:
        id.append(issue.id)
        vendors.append(issue.custom_fields[0].value)
        models.append(issue.custom_fields[1].value)
        orders.append(issue.custom_fields[2].value)
        contracts.append(issue.custom_fields[3].value)
    shipments = zip(id, vendors, models, orders, contracts)
    return render(request, 'shipment/shipment_list.html', {'shipments': shipments})


@login_required
def shipment_create_report(request, shipment_id):
    redmine = Redmine(settings.HQ_REDMINE_URL, username=settings.HQ_REDMINE_USERNAME,
                      password=settings.HQ_REDMINE_PASSWORD)
    issue = redmine.issue.get(shipment_id)
    vendor = issue.custom_fields[0].value
    model = issue.custom_fields[1].value
    order = issue.custom_fields[2].value
    contract = issue.custom_fields[3].value

    # генерируем протокол входного контроля
    protocol_file = DocxTemplate("docx_templates/protocol_shipment.docx")

    context = {'vendor': vendor, 'model': model, 'order': order, 'contract': contract}
    protocol_file.render(context)
    protocol_filename = 'Protocol_of_shipment_' + str(issue.id) + '.docx'
    protocol_file.save(protocol_filename)
    # возвращаем ПМИ
    file_path = os.path.join(settings.MEDIA_ROOT, protocol_filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
