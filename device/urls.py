from django.urls import path
from . import views


urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('device/create/', views.device_create, name='device_create'),
    path('delete/<int:device_id>/', views.device_delete, name='device_delete'),
    path('<int:device_id>/', views.device_edit, name='device_edit'),
    path('export/<int:device_id>', views.device_export, name='device_export'),
    path('import/', views.device_import, name='device_import'),

    path('type/', views.DeviceTypeListView.as_view(), name='device_types'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/update/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/delete/<int:pk>/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),
    path('type/details/<int:pk>/', views.device_type_details, name='device_type_details'),
]
