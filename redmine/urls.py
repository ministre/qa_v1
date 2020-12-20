from django.urls import path
from . import views

urlpatterns = [
    path('device_type/export', views.redmine_device_type_export, name='redmine_device_type_export'),
    path('device/export', views.redmine_device_export, name='redmine_device_export'),
    path('protocol/export', views.redmine_protocol_export, name='redmine_protocol_export'),
]
