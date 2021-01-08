from django.contrib.auth.decorators import login_required
from device.models import DeviceType, Device
from protocol.models import Protocol, TestResult
from .models import RedmineDeviceType, RedmineDevice, RedmineProtocol, RedmineResult
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError


@login_required
def redmine_device_type_export(request):
    if request.method == "POST":
        device_type = get_object_or_404(DeviceType, id=request.POST['device_type_id'])
        back_url = reverse('device_type_details', kwargs={'pk': device_type.id, 'tab_id': 2})
        general_info = False
        try:
            if request.POST['general_info']:
                general_info = True
        except MultiValueDictKeyError:
            pass
        message = RedmineDeviceType.export(device_type=device_type, project=request.POST['redmine_project'],
                                           project_name=request.POST['redmine_project_name'],
                                           project_desc=request.POST['redmine_project_desc'],
                                           project_parent=request.POST['redmine_parent'],
                                           general_info=general_info)
    else:
        message = [False, _('Page not found')]
        back_url = reverse('device_types')
    return render(request, 'redmine/message.html', {'message': message, 'back_url': back_url})


@login_required
def redmine_device_export(request):
    if request.method == "POST":
        device = get_object_or_404(Device, id=request.POST['device_id'])
        back_url = reverse('device_details', kwargs={'pk': device.id, 'tab_id': 2})
        general = photos = samples = protocols = False
        try:
            if request.POST['general']:
                general = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['protocols']:
                protocols = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['photos']:
                photos = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['samples']:
                samples = True
        except MultiValueDictKeyError:
            pass
        message = RedmineDevice.export(device=device, project=request.POST['redmine_project'],
                                       project_name=request.POST['redmine_project_name'],
                                       project_desc=request.POST['redmine_project_desc'],
                                       project_parent=request.POST['redmine_parent'],
                                       general=general, photos=photos, samples=samples, protocols=protocols)
    else:
        message = [False, _('Page not found')]
        back_url = reverse('devices')
    return render(request, 'redmine/message.html', {'message': message, 'back_url': back_url})


@login_required
def redmine_protocol_export(request):
    if request.method == "POST":
        protocol = get_object_or_404(Protocol, id=request.POST['protocol_id'])
        back_url = reverse('protocol_details', kwargs={'pk': protocol.id, 'tab_id': 5})
        general = results = False
        try:
            if request.POST['general']:
                general = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['results']:
                results = True
        except MultiValueDictKeyError:
            pass
        message = RedmineProtocol.export(protocol=protocol, project=request.POST['redmine_project'],
                                         project_wiki=request.POST['redmine_wiki'], general=general, results=results)
    else:
        message = [False, _('Page not found')]
        back_url = reverse('protocols')
    return render(request, 'redmine/message.html', {'message': message, 'back_url': back_url})


@login_required
def redmine_result_export(request):
    if request.method == "POST":
        result = get_object_or_404(TestResult, id=request.POST['result_id'])
        back_url = reverse('result_details', kwargs={'pk': result.id, 'tab_id': 7})
        test_desc = result_notes = result_configs = result_images = result_summary = False
        try:
            if request.POST['test_desc']:
                test_desc = True
            if request.POST['result_notes']:
                result_notes = True
            if request.POST['result_configs']:
                result_configs = True
            if request.POST['result_images']:
                result_images = True
            if request.POST['result_summary']:
                result_summary = True
        except MultiValueDictKeyError:
            pass
        message = RedmineResult.export(result=result, project=request.POST['redmine_project'],
                                       project_wiki=request.POST['redmine_wiki'],
                                       project_parent_wiki=request.POST['redmine_parent_wiki'],
                                       test_desc=test_desc,
                                       result_notes=result_notes,
                                       result_configs=result_configs,
                                       result_images=result_images,
                                       result_summary=result_summary)
    else:
        message = [False, _('Page not found')]
        back_url = reverse('protocols')
    return render(request, 'redmine/message.html', {'message': message, 'back_url': back_url})
