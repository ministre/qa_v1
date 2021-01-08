from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from qa_v1 import settings
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
import re
from device.models import Vendor, Device, DeviceType, DevicePhoto, DeviceSample, DeviceSampleAccount
from django.http import HttpResponseRedirect
from .forms import VendorForm, DeviceTypeForm, DeviceForm, DevicePhotoForm, DeviceSampleForm, DeviceSampleAccountForm
from redmine.forms import RedmineDeviceTypeExportForm, RedmineDeviceExportForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils import timezone


class Item(object):
    @staticmethod
    def update_timestamp(foo, user):
        foo.updated_by = user
        foo.updated_at = timezone.now()
        foo.save()

    @staticmethod
    def set_priority(foo, priority: int):
        foo.priority = priority
        foo.save()


@method_decorator(login_required, name='dispatch')
class VendorListView(ListView):
    context_object_name = 'vendors'
    queryset = Vendor.objects.all().order_by('name')
    template_name = 'device/vendors.html'


@method_decorator(login_required, name='dispatch')
class VendorCreate(CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('vendors')
        return context

    def get_success_url(self):
        return reverse('vendors')


@method_decorator(login_required, name='dispatch')
class VendorUpdate(UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('vendor_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('vendor_details', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class VendorDelete(DeleteView):
    model = Vendor
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('vendor_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('vendors')


@login_required
def vendor_details(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    devices_count = vendor.devices_count()
    return render(request, 'device/vendor_details.html', {'vendor': vendor, 'devices_count': devices_count})


@method_decorator(login_required, name='dispatch')
class DeviceTypeListView(ListView):
    context_object_name = 'device_types'
    queryset = DeviceType.objects.all().order_by("name")
    template_name = 'device/device_types.html'


@method_decorator(login_required, name='dispatch')
class DeviceTypeCreate(CreateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_types')
        return context

    def get_success_url(self):
        return reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceTypeUpdate(UpdateView):
    model = DeviceType
    form_class = DeviceTypeForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceTypeDelete(DeleteView):
    model = DeviceType
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_type_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('device_types')


@login_required
def device_type_details(request, pk, tab_id):
    device_type = get_object_or_404(DeviceType, id=pk)
    devices_count = device_type.devices_count()
    redmine_url = settings.REDMINE_URL
    export_form = RedmineDeviceTypeExportForm(initial={'device_type_id': device_type.id,
                                                       'redmine_project': device_type.redmine_project,
                                                       'redmine_project_name': device_type.redmine_project_name,
                                                       'redmine_project_desc': device_type.redmine_project_desc,
                                                       'redmine_parent': device_type.redmine_parent,
                                                       'general_info': True})
    return render(request, 'device/device_type_details.html', {'device_type': device_type,
                                                               'devices_count': devices_count,
                                                               'redmine_url': redmine_url,
                                                               'export_form': export_form,
                                                               'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class DeviceListView(ListView):
    context_object_name = 'devices'
    queryset = Device.objects.all().order_by("-id")
    template_name = 'device/devices.html'


@method_decorator(login_required, name='dispatch')
class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('devices')
        return context

    def get_success_url(self):
        if not self.object.redmine_parent:
            if self.object.type.redmine_project:
                self.object.redmine_parent = self.object.type.redmine_project
                self.object.save()
        if not self.object.redmine_project_name:
            self.object.redmine_project_name = str(self.object.vendor) + ' ' + str(self.object.model)
            self.object.save()
        return reverse('devices')


@method_decorator(login_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        if not self.object.redmine_parent:
            if self.object.type.redmine_project:
                self.object.redmine_parent = self.object.type.redmine_project
                self.object.save()
        if not self.object.redmine_project_name:
            self.object.redmine_project_name = str(self.object.vendor) + ' ' + str(self.object.model)
            self.object.save()
        return reverse('device_details', kwargs={'pk': self.object.id, 'tab_id': 1})


@method_decorator(login_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
        return reverse('devices')


@login_required
def device_details(request, pk, tab_id):
    device = get_object_or_404(Device, id=pk)
    protocols_count = device.protocols_count()
    redmine_url = settings.REDMINE_URL
    export_form = RedmineDeviceExportForm(initial={'device_id': device.id,
                                                   'redmine_project': device.redmine_project,
                                                   'redmine_project_name': device.redmine_project_name,
                                                   'redmine_project_desc': device.redmine_project_desc,
                                                   'redmine_parent': device.redmine_parent,
                                                   'general_info': True, 'protocols': True})
    return render(request, 'device/device_details.html', {'device': device, 'protocols_count': protocols_count,
                                                          'redmine_url': redmine_url, 'export_form': export_form,
                                                          'tab_id': tab_id})


@method_decorator(login_required, name='dispatch')
class DevicePhotoCreate(CreateView):
    model = DevicePhoto
    form_class = DevicePhotoForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 3})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class DevicePhotoUpdate(UpdateView):
    model = DevicePhoto
    form_class = DevicePhotoForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class DevicePhotoDelete(DeleteView):
    model = DevicePhoto
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 3})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 3})


@method_decorator(login_required, name='dispatch')
class DeviceSampleCreate(CreateView):
    model = DeviceSample
    form_class = DeviceSampleForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DeviceSampleUpdate(UpdateView):
    model = DeviceSample
    form_class = DeviceSampleForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DeviceSampleDelete(DeleteView):
    model = DeviceSample
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DeviceSampleAccountCreate(CreateView):
    model = DeviceSampleAccount
    form_class = DeviceSampleAccountForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'sample': self.kwargs.get('sample_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample = get_object_or_404(DeviceSample, id=self.kwargs.get('sample_id'))
        context['back_url'] = reverse('device_details', kwargs={'pk': sample.device.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.sample.device.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DeviceSampleAccountUpdate(UpdateView):
    model = DeviceSampleAccount
    form_class = DeviceSampleAccountForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.sample.device.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.sample.device.id, 'tab_id': 4})


@method_decorator(login_required, name='dispatch')
class DeviceSampleAccountDelete(DeleteView):
    model = DeviceSampleAccount
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.sample.device.id, 'tab_id': 4})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.sample.device.id, 'tab_id': 4})


@login_required
def device_import(request):
    if request.method == 'POST':
        project_id = request.POST['project_id']
        redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.1.1')
        if project_id == '':
            error = 'Отсутствует идентификатор проекта!'
            return render(request, 'device/device_import_error.html', {'error': error})
        try:
            project = redmine.project.get(project_id)
            try:
                wiki_page = redmine.wiki_page.get('Wiki', project_id=project.id)
                # парсим wiki-страницу
                # тип устройства
                blocks = wiki_page.text.split('h2. ')
                tag_blocks = blocks[0].split('#')
                vendor = ''
                model = ''
                hw = ''
                interfaces = ''
                leds = ''
                buttons = ''
                chipsets = ''
                memory = ''
                try:
                    device_type_id = DeviceType.objects.filter(Q(main_type=tag_blocks[1]) & Q(sub_type=tag_blocks[2]))[0].id
                except IndexError:
                    error = 'Неизвестный тип устройства!'
                    return render(request, 'device/device_import_error.html', {'error': error})
                # параметры устройства
                for i, block in enumerate(blocks):
                    parser = re.search('Общая информация', block)
                    if parser:
                        device_blocks = blocks[i].split('|')
                        for j, device_block in enumerate(device_blocks):
                            parser = re.search('Производитель:', device_block)
                            if parser:
                                vendor = device_blocks[j + 1][1:-1]
                        for j, device_block in enumerate(device_blocks):
                            parser = re.search('Модель:', device_block)
                            if parser:
                                model = device_blocks[j + 1][1:-1]
                        for j, device_block in enumerate(device_blocks):
                            parser = re.search('Версия Hardware:', device_block)
                            if parser:
                                hw = device_blocks[j + 1][1:-1]
                        for j, device_block in enumerate(device_blocks):
                            parser = re.search('Интерфейсы:', device_block)
                            if parser:
                                interfaces = device_blocks[j + 1][1:-1]
                        for j, device_block in enumerate(device_blocks):
                            parser = re.search('Индикаторы:', device_block)
                            if parser:
                                leds = device_blocks[j + 1][1:-1]
                        for j, device_block in enumerate(device_blocks):
                            parser = re.search('Кнопки:', device_block)
                            if parser:
                                buttons = device_blocks[j + 1][1:-1]
                        for j, device_block in enumerate(device_blocks):
                            parser = re.search('Чипсеты:', device_block)
                            if parser:
                                chipsets = device_blocks[j + 1][1:-1]
                        for j, device_block in enumerate(device_blocks):
                            parser = re.search('Память:', device_block)
                            if parser:
                                memory = device_blocks[j + 1][1:-1]
                new_device = Device(project_id=project_id, type=DeviceType.objects.get(id=device_type_id),
                                    vendor=vendor, model=model, hw=hw, interfaces=interfaces, leds=leds,
                                    buttons=buttons, chipsets=chipsets, memory=memory)
                new_device.save()
                return HttpResponseRedirect('/device/')
            except ResourceNotFoundError:
                error = 'Отсутствует Wiki-страница!'
                return render(request, 'device/device_import_error.html', {'error': error})
        except ResourceNotFoundError:
            error = 'Проект не найден!'
            return render(request, 'device/device_import_error.html', {'error': error})
    else:
        return render(request, 'device/device_import.html')
