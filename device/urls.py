from django.urls import path
from . import views


urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('device/create/', views.device_create, name='device_create'),
    path('delete/<int:device_id>/', views.device_delete, name='device_delete'),
    path('<int:device_id>/', views.device_edit, name='device_edit'),
    path('export/<int:device_id>', views.device_export, name='device_export'),
    path('import/', views.device_import, name='device_import'),
    path('type/', views.device_type_list, name='device_type_list'),
    path('type/create/', views.device_type_create, name='device_type_create'),
    path('type/delete/<int:device_type_id>/', views.device_type_delete, name='device_type_delete'),
    path('type/<int:device_type_id>/', views.device_type_edit, name='device_type_edit'),
]
