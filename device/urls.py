from django.urls import path
from . import views


urlpatterns = [
    path('', views.DeviceListView.as_view(), name='devices'),
    # vendors
    path('vendors/', views.VendorListView.as_view(), name='vendors'),
    path('vendor/create/', views.VendorCreate.as_view(), name='vendor_create'),
    path('vendor/update/<int:pk>/', views.VendorUpdate.as_view(), name='vendor_update'),
    path('vendor/delete/<int:pk>/', views.VendorDelete.as_view(), name='vendor_delete'),
    path('vendor/<int:pk>/', views.vendor_details, name='vendor_details'),
    # device types
    path('type/', views.DeviceTypeListView.as_view(), name='device_types'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/update/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/delete/<int:pk>/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),
    path('type/details/<int:pk>/<int:tab_id>', views.device_type_details, name='device_type_details'),
    # devices
    path('create/', views.DeviceCreate.as_view(), name='device_create'),
    path('update/<int:pk>/', views.DeviceUpdate.as_view(), name='device_update'),
    path('delete/<int:pk>/', views.DeviceDelete.as_view(), name='device_delete'),
    path('details/<int:pk>/<int:tab_id>', views.device_details, name='device_details'),
    # samples
    path('sample/create/<int:device_id>', views.DeviceSampleCreate.as_view(), name='sample_create'),
    path('sample/update/<int:pk>/', views.DeviceSampleUpdate.as_view(), name='sample_update'),
    path('sample/delete/<int:pk>/', views.DeviceSampleDelete.as_view(), name='sample_delete'),
    path('sample/account/create/<int:sample_id>', views.DeviceSampleAccountCreate.as_view(), name='sample_acc_create'),
    path('sample/account/update/<int:pk>', views.DeviceSampleAccountUpdate.as_view(), name='sample_acc_update'),
    path('sample/account/delete/<int:pk>', views.DeviceSampleAccountDelete.as_view(), name='sample_acc_delete'),
]
