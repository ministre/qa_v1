from django.urls import path
from . import views

urlpatterns = [
    path('device_type/export', views.redmine_device_type_export, name='redmine_device_type_export'),
]
