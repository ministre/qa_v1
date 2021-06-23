from django.urls import path
from . import views


urlpatterns = [
    path('', views.DeviceListView.as_view(), name='devices'),
    # vendors
    path('vendor/', views.VendorListView.as_view(), name='vendors'),
    path('vendor/create/', views.VendorCreate.as_view(), name='vendor_create'),
    path('vendor/update/<int:pk>/', views.VendorUpdate.as_view(), name='vendor_update'),
    path('vendor/delete/<int:pk>/', views.VendorDelete.as_view(), name='vendor_delete'),
    path('vendor/<int:pk>/', views.vendor_details, name='vendor_details'),
    # device types
    path('type/', views.DeviceTypeListView.as_view(), name='device_types'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/update/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/delete/<int:pk>/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),
    path('type/details/<int:pk>/<int:tab_id>/', views.device_type_details, name='device_type_details'),
    # devices
    path('create/', views.DeviceCreate.as_view(), name='device_create'),
    path('update/<int:pk>/', views.DeviceUpdate.as_view(), name='device_update'),
    path('delete/<int:pk>/', views.DeviceDelete.as_view(), name='device_delete'),
    path('details/<int:pk>/<int:tab_id>/', views.device_details, name='device_details'),
    # photos
    path('photo/create/<int:device_id>/', views.DevicePhotoCreate.as_view(), name='photo_create'),
    path('photo/update/<int:pk>/', views.DevicePhotoUpdate.as_view(), name='photo_update'),
    path('photo/delete/<int:pk>/', views.DevicePhotoDelete.as_view(), name='photo_delete'),
    # samples
    path('sample/create/<int:device_id>/', views.DeviceSampleCreate.as_view(), name='sample_create'),
    path('sample/update/<int:pk>/', views.DeviceSampleUpdate.as_view(), name='sample_update'),
    path('sample/delete/<int:pk>/', views.DeviceSampleDelete.as_view(), name='sample_delete'),
    path('sample/account/create/<int:sample_id>/', views.DeviceSampleAccountCreate.as_view(), name='sample_acc_create'),
    path('sample/account/update/<int:pk>/', views.DeviceSampleAccountUpdate.as_view(), name='sample_acc_update'),
    path('sample/account/delete/<int:pk>/', views.DeviceSampleAccountDelete.as_view(), name='sample_acc_delete'),
    # files
    path('file/create/<int:device_id>/', views.DeviceFileCreate.as_view(), name='file_create'),
    path('file/update/<int:pk>/', views.DeviceFileUpdate.as_view(), name='file_update'),
    path('file/delete/<int:pk>/', views.DeviceFileDelete.as_view(), name='file_delete'),
    # notes
    path('note/create/<int:device_id>/', views.DeviceNoteCreate.as_view(), name='note_create'),
    path('note/update/<int:pk>/', views.DeviceNoteUpdate.as_view(), name='note_update'),
    path('note/delete/<int:pk>/', views.DeviceNoteDelete.as_view(), name='note_delete'),
    # contacts
    path('contact/create/<int:device_id>/', views.DeviceContactCreate.as_view(), name='d_contact_create'),
    path('contact/delete/<int:pk>/', views.DeviceContactDelete.as_view(), name='d_contact_delete'),
    # chipsets
    path('chipset/', views.ChipsetListView.as_view(), name='chipsets'),
    path('chipset/create/', views.ChipsetCreate.as_view(), name='chipset_create'),
    path('chipset/update/<int:pk>/', views.ChipsetUpdate.as_view(), name='chipset_update'),
    path('chipset/delete/<int:pk>/', views.ChipsetDelete.as_view(), name='chipset_delete'),
    path('chipset/<int:pk>/', views.chipset_details, name='chipset_details'),
    # chipsets devices
    path('device-chipset/add/<int:device_id>/<int:chipset_id>/', views.device_chipset_add, name='device-chipset_add'),
    path('device-chipset/create_add/<int:device_id>/', views.device_chipset_create_add,
         name='device-chipset_create_add'),
    path('device-chipset/delete/<int:pk>/', views.DeviceChipsetDelete.as_view(), name='device-chipset_delete'),
]
