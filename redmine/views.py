from django.contrib.auth.decorators import login_required
from device.models import DeviceType
from .models import RedmineProject, RedmineDeviceType
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
