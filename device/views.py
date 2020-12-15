from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from qa_v1 import settings
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
import re
from device.models import Device, DeviceType
from django.http import HttpResponseRedirect
from .forms import DeviceTypeForm, DeviceForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils import timezone


@method_decorator(login_required, name='dispatch')
class DeviceTypeListView(ListView):
    context_object_name = 'device_types'
    queryset = DeviceType.objects.all().order_by("-id")
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
    redmine_url = settings.REDMINE_URL
    devices_count = device_type.devices_count()
    return render(request, 'device/device_type_details.html', {'device_type': device_type,
                                                               'devices_count': devices_count,
                                                               'redmine_url': redmine_url,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('devices')
        return context

    def get_success_url(self):
        return reverse('devices')


@method_decorator(login_required, name='dispatch')
class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.id, 'tab_id': 1})
        return context

    def get_success_url(self):
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
    return render(request, 'device/device_details.html', {'device': device, 'tab_id': tab_id})


@login_required
def device_export(request, pk):
    device = get_object_or_404(Device, id=pk)
    redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY, version='4.1.1')
    try:
        # если проект существует
        project = redmine.project.get(device.project_id)
        redmine.project.update(device.project_id, name=device.vendor + ' ' + device.model)
        try:
            wiki_page = redmine.wiki_page.get('Wiki', project_id=project.id)
            blocks = wiki_page.text.split('h2. ')
            for i, block in enumerate(blocks):
                parser = re.search('Общая информация', block)
                if parser:
                    device_info = '| Производитель: | ' + device.vendor + ' |\n' \
                                      '| Модель: | ' + device.model + ' |\n' \
                                      '| Версия Hardware: | ' + device.hw + ' |\n'
                    if device.interfaces != '':
                        device_info = device_info + '| Интерфейсы: | ' + device.interfaces + ' |\n'
                    if device.leds != '':
                        device_info = device_info + '| Индикаторы: | ' + device.leds + ' |\n'
                    if device.buttons != '':
                        device_info = device_info + '| Кнопки: | ' + device.buttons + ' |\n'
                    if device.chipsets != '':
                        device_info = device_info + '| Чипсеты: | ' + device.chipsets + ' |\n'
                    if device.memory != '':
                        device_info = device_info + '| Память: | ' + device.memory + ' |\n'
                    blocks[i] = 'Общая информация \n\n' + device_info + '\n\n'
            blocks[0] = '__%{color:white} #' + device.type.main_type + '#' + device.type.sub_type \
                        + '#%__\n\n---\n\nh1. ' + device.vendor + ' ' + device.model + '\n\n'
            new_wiki_page = 'h2. '.join(blocks)
            redmine.wiki_page.update('Wiki', project_id=project.id, text=new_wiki_page)
            return HttpResponseRedirect('/device/')
        except ResourceNotFoundError:
            return HttpResponseRedirect('/')

    except ResourceNotFoundError:
        # если проект не найден, создаем его
        parent_id = redmine.project.get(device.type.main_type).id
        project = redmine.project.create(
            name=device.vendor + ' ' + device.model,
            identifier=device.project_id,
            parent_id=parent_id,
            inherit_members=True
        )
        new_wiki_page = '__%{color:white} #' + device.type.main_type + \
                        '#' + device.type.sub_type + '#%__\n\n---\n\nh1. ' + device.vendor + ' ' \
                        + device.model + '\n\nh2. Внешний вид\n\nh2. Общая информация\n\n| Производитель: | ' +\
                        device.vendor + ' |\n| Модель: | ' +\
                        device.model + ' |\n| Версия Hardware: | ' + device.hw + ' |\n'
        if device.interfaces != '':
            new_wiki_page = new_wiki_page + '| Интерфейсы: | ' + device.interfaces + ' |\n'
        if device.leds != '':
            new_wiki_page = new_wiki_page + '| Индикаторы: | ' + device.leds + ' |\n'
        if device.buttons != '':
            new_wiki_page = new_wiki_page + '| Кнопки: | ' + device.buttons + ' |\n'
        if device.chipsets != '':
            new_wiki_page = new_wiki_page + '| Чипсеты: | ' + device.chipsets + ' |\n'
        if device.memory != '':
            new_wiki_page = new_wiki_page + '| Память: | ' + device.memory + ' |\n'
        new_wiki_page = new_wiki_page + '\nh2. Результаты испытаний\n'
        redmine.wiki_page.update('Wiki', project_id=device.project_id, text=new_wiki_page)
        return HttpResponseRedirect('/device/')


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
