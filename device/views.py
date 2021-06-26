from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from qa_v1 import settings
from device.models import Vendor, Device, DeviceType, DevicePhoto, DeviceSample, DeviceSampleAccount, DeviceFile, \
    DeviceNote, DeviceContact, Chipset, DeviceChipset
from contact.models import Contact
from .forms import VendorForm, DeviceTypeForm, DeviceForm, DevicePhotoForm, DeviceSampleForm, DeviceSampleAccountForm, \
    DeviceFileForm, DeviceNoteForm, DeviceContactForm, ChipsetForm
from redmine.forms import RedmineDeviceTypeExportForm, RedmineDeviceExportForm
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils import timezone
import textile
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django import forms


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
    chipsets = device.get_chipsets()
    all_chipsets = []
    for chipset in Chipset.objects.all():
        all_chipsets.append({'id': chipset.id, 'name': str(chipset), 'type': chipset.get_type_as_string()})

    notes = DeviceNote.objects.filter(device=device).order_by('id')
    converted_notes = []
    for note in notes:
        if note.format == 0:
            converted_note = {'id': note.id, 'desc': note.desc, 'text': textile.textile(note.text),
                              'format': note.format}
        else:
            converted_note = {'id': note.id, 'desc': note.desc, 'text': note.text,
                              'format': note.format}
        converted_notes.append(converted_note)

    chipset_form = ChipsetForm()
    chipset_form.fields['datasheet'].widget = forms.HiddenInput()

    redmine_url = settings.REDMINE_URL
    export_form = RedmineDeviceExportForm(initial={'device_id': device.id,
                                                   'redmine_project': device.redmine_project,
                                                   'redmine_project_name': device.redmine_project_name,
                                                   'redmine_project_desc': device.redmine_project_desc,
                                                   'redmine_parent': device.redmine_parent})
    return render(request, 'device/device_details.html', {
        'device': device,
        'chipsets': chipsets,
        'all_chipsets': all_chipsets,
        'protocols_count': protocols_count,
        'notes': converted_notes,
        'chipset_form': chipset_form,
        'redmine_url': redmine_url,
        'export_form': export_form,
        'tab_id': tab_id
    })


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


@method_decorator(login_required, name='dispatch')
class DeviceFileCreate(CreateView):
    model = DeviceFile
    form_class = DeviceFileForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class DeviceFileUpdate(UpdateView):
    model = DeviceFile
    form_class = DeviceFileForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class DeviceFileDelete(DeleteView):
    model = DeviceFile
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 5})


@method_decorator(login_required, name='dispatch')
class DeviceNoteCreate(CreateView):
    model = DeviceNote
    form_class = DeviceNoteForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class DeviceNoteUpdate(UpdateView):
    model = DeviceNote
    form_class = DeviceNoteForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class DeviceNoteDelete(DeleteView):
    model = DeviceNote
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 6})


@method_decorator(login_required, name='dispatch')
class DeviceContactCreate(CreateView):
    model = DeviceContact
    form_class = DeviceContactForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'device': self.kwargs.get('device_id'),
                'created_by': self.request.user, 'updated_by': self.request.user}

    def get_form(self, form_class=DeviceContactForm):
        form = super(DeviceContactCreate, self).get_form(form_class)
        form.fields['contact'].queryset = Contact.objects.exclude(vendor__isnull=True).order_by('last_name')
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.kwargs.get('device_id'), 'tab_id': 7})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 7})


@method_decorator(login_required, name='dispatch')
class DeviceContactDelete(DeleteView):
    model = DeviceContact
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 7})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 7})


@login_required
def chipsets(request):
    chipset_list = []
    for chipset in Chipset.objects.all():
        chipset_list.append({'id': chipset.id, 'vendor': chipset.vendor, 'model': chipset.model,
                             'type': chipset.get_type_as_string(), 'desc': chipset.desc})
    return render(request, 'device/chipsets.html', {'chipsets': chipset_list})


@method_decorator(login_required, name='dispatch')
class ChipsetCreate(CreateView):
    model = Chipset
    form_class = ChipsetForm
    template_name = 'device/create.html'

    def get_initial(self):
        return {'created_by': self.request.user, 'updated_by': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('chipsets')
        return context

    def get_success_url(self):
        return reverse('chipsets')


@method_decorator(login_required, name='dispatch')
class ChipsetUpdate(UpdateView):
    model = Chipset
    form_class = ChipsetForm
    template_name = 'device/update.html'

    def get_initial(self):
        return {'updated_by': self.request.user, 'updated_at': timezone.now()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('chipset_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('chipset_details', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class ChipsetDelete(DeleteView):
    model = Chipset
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('chipset_details', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('chipsets')


@login_required
def chipset_details(request, pk):
    chipset = get_object_or_404(Chipset, id=pk)
    chipset_type = chipset.get_type_as_string()
    devices = chipset.get_devices()
    return render(request, 'device/chipset_details.html', {'chipset': chipset, 'type': chipset_type,
                                                           'devices': devices})


@login_required
def device_chipset_add(request, device_id: int, chipset_id: int):
    device = get_object_or_404(Device, id=device_id)
    chipset = get_object_or_404(Chipset, id=chipset_id)
    device_chipset = DeviceChipset(device=device, chipset=chipset, created_by=request.user, updated_by=request.user)
    device_chipset.save()
    return HttpResponseRedirect(reverse('device_details', kwargs={'pk': device.id, 'tab_id': 2}))


@login_required
def device_chipset_create_add(request, device_id: int):
    if request.method == "POST":
        device = get_object_or_404(Device, id=device_id)
        form = ChipsetForm(request.POST)
        if form.is_valid():
            new_chipset = Chipset.objects.create(vendor=form.cleaned_data['vendor'], model=form.cleaned_data['model'],
                                                 type=form.cleaned_data['type'], desc=form.cleaned_data['desc'],
                                                 created_by=request.user, updated_by=request.user)
            chipset = get_object_or_404(Chipset, id=new_chipset.id)
            DeviceChipset.objects.create(device=device, chipset=chipset, created_by=request.user,
                                         updated_by=request.user)
            return HttpResponseRedirect(reverse('device_details', kwargs={'pk': device.id, 'tab_id': 2}))
    else:
        return render(request, 'device/message.html', {'message': [False, _('Page not found')]})


@method_decorator(login_required, name='dispatch')
class DeviceChipsetDelete(DeleteView):
    model = DeviceChipset
    template_name = 'device/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 2})
        return context

    def get_success_url(self):
        return reverse('device_details', kwargs={'pk': self.object.device.id, 'tab_id': 2})
