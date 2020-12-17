from device.models import DeviceType
from .models import RedmineProject
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


def redmine_device_type_export(request):
    if request.method == "POST":
        device_type = get_object_or_404(DeviceType, id=request.POST['device_type_id'])
        back_url = reverse('device_type_details', kwargs={'pk': device_type.id, 'tab_id': 2})
        redmine_project = request.POST['redmine_project']
        # check project
        is_project = RedmineProject().check_project(redmine_project=redmine_project)
        if not is_project[0]:
            return render(request, 'redmine/message.html', {'message': is_project, 'back_url': back_url})
        # do something
        return render(request, 'redmine/message.html', {'message': [True, 'test'], 'back_url': back_url})
    else:
        message = [False, _('Page not found')]
        back_url = reverse('device_types')
    return render(request, 'redmine/message.html', {'message': message, 'back_url': back_url})
