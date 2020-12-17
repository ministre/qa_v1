from django.urls import path
from . import views


urlpatterns = [
    path('', views.DeviceListView.as_view(), name='devices'),

    # Vendors
    path('vendors/', views.VendorListView.as_view(), name='vendors'),
    path('vendor/create/', views.VendorCreate.as_view(), name='vendor_create'),
    path('vendor/update/<int:pk>/', views.VendorUpdate.as_view(), name='vendor_update'),
    path('vendor/delete/<int:pk>/', views.VendorDelete.as_view(), name='vendor_delete'),
    path('vendor/<int:pk>/', views.vendor_details, name='vendor_details'),

    # Device Types
    path('type/', views.DeviceTypeListView.as_view(), name='device_types'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/update/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/delete/<int:pk>/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),
    path('type/details/<int:pk>/<int:tab_id>', views.device_type_details, name='device_type_details'),

    # Devices
    path('create/', views.DeviceCreate.as_view(), name='device_create'),
    path('update/<int:pk>/', views.DeviceUpdate.as_view(), name='device_update'),
    path('delete/<int:pk>/', views.DeviceDelete.as_view(), name='device_delete'),
    path('details/<int:pk>/<int:tab_id>', views.device_details, name='device_details'),

    # Redmine
    path('export/<int:pk>', views.device_export, name='device_export'),
    path('import/', views.device_import, name='device_import'),
]
