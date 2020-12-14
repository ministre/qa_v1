from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from qa_v1 import settings
from redminelib import Redmine
from django.conf import settings


@login_required
def shipments(request):
    redmine = Redmine(settings.HQ_REDMINE_URL, key=settings.HQ_REDMINE_KEY)
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
    tickets = zip(id, vendors, models, orders, contracts)
    return render(request, 'shipment/shipments.html', {'shipments': tickets,
                                                       'redmine_url': settings.HQ_REDMINE_URL})
