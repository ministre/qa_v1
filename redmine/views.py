from django.contrib.auth.decorators import login_required
from device.models import DeviceType, Device
from testplan.models import Test, TestPlan
from protocol.models import Protocol, TestResult
from .models import RedmineDeviceType, RedmineDevice, RedmineTest, RedmineTestplan, RedmineProtocol, RedmineResult
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
    return render(request, 'device/message.html', {'message': message, 'back_url': back_url})


@login_required
def redmine_device_export(request):
    if request.method == "POST":
        device = get_object_or_404(Device, id=request.POST['device_id'])
        back_url = reverse('device_details', kwargs={'pk': device.id, 'tab_id': 7})
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
    return render(request, 'device/message.html', {'message': message, 'back_url': back_url})


@login_required
def redmine_test_export(request):
    if request.method == "POST":
        test = get_object_or_404(Test, id=request.POST['test_id'])
        configs = images = files = links = comments = False
        try:
            if request.POST['configs']:
                configs = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['images']:
                images = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['files']:
                files = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['links']:
                links = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['comments']:
                comments = True
        except MultiValueDictKeyError:
            pass
        message = RedmineTest.export(test=test,
                                     project=request.POST['redmine_project'],
                                     project_wiki=request.POST['redmine_wiki'],
                                     configs=configs,
                                     images=images,
                                     files=files,
                                     links=links,
                                     comments=comments)
        back_url = reverse('test_details', kwargs={'pk': test.id, 'tab_id': 8})
        return render(request, 'device/message.html', {'message': message, 'back_url': back_url})
    else:
        return render(request, 'device/message.html', {'message': [False, _('Page not found')]})


@login_required
def redmine_testplan_export(request):
    if request.method == "POST":
        testplan = get_object_or_404(TestPlan, id=request.POST['testplan_id'])
        test_list = test_details_wiki = False
        try:
            if request.POST['test_list']:
                test_list = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['test_details_wiki']:
                test_details_wiki = True
        except MultiValueDictKeyError:
            pass
        message = RedmineTestplan.export(testplan=testplan, project=request.POST['redmine_project'],
                                         project_name=request.POST['redmine_project_name'],
                                         project_desc=request.POST['redmine_project_desc'],
                                         project_parent=request.POST['redmine_parent'],
                                         test_list=test_list,
                                         test_details_wiki=test_details_wiki)
        back_url = reverse('testplan_details', kwargs={'pk': testplan.id, 'tab_id': 4})
        return render(request, 'device/message.html', {'message': message, 'back_url': back_url})
    else:
        return render(request, 'device/message.html', {'message': [False, _('Page not found')]})


@login_required
def redmine_result_export(request):
    if request.method == "POST":
        result = get_object_or_404(TestResult, id=request.POST['result_id'])
        back_url = reverse('result_details', kwargs={'pk': result.id, 'tab_id': 8})
        test_desc = result_notes = result_configs = result_images = result_files = result_summary = False
        try:
            if request.POST['test_desc']:
                test_desc = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['result_notes']:
                result_notes = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['result_configs']:
                result_configs = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['result_images']:
                result_images = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['result_files']:
                result_files = True
        except MultiValueDictKeyError:
            pass
        try:
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
                                       result_files=result_files,
                                       result_summary=result_summary)
    else:
        message = [False, _('Page not found')]
        back_url = reverse('protocols')
    return render(request, 'device/message.html', {'message': message, 'back_url': back_url})


@login_required
def redmine_protocol_export(request):
    if request.method == "POST":
        protocol = get_object_or_404(Protocol, id=request.POST['protocol_id'])
        back_url = reverse('protocol_details', kwargs={'pk': protocol.id, 'tab_id': 5})
        general = results_list = results_wiki = False
        try:
            if request.POST['general']:
                general = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['results_list']:
                results_list = True
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['results_wiki']:
                results_wiki = True
        except MultiValueDictKeyError:
            pass
        message = RedmineProtocol.export(protocol=protocol, project=request.POST['redmine_project'],
                                         project_wiki=request.POST['redmine_wiki'],
                                         general=general,
                                         results_list=results_list,
                                         results_wiki=results_wiki)
    else:
        message = [False, _('Page not found')]
        back_url = reverse('protocols')
    return render(request, 'device/message.html', {'message': message, 'back_url': back_url})
