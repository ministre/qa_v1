from django.urls import path
from . import views

urlpatterns = [
    path('device_type/export', views.redmine_device_type_export, name='redmine_device_type_export'),
    path('device/export', views.redmine_device_export, name='redmine_device_export'),
    path('test/export', views.redmine_test_export, name='redmine_test_export'),
    path('testplan/export', views.redmine_testplan_export, name='redmine_testplan_export'),
    path('protocol/export', views.redmine_protocol_export, name='redmine_protocol_export'),
    path('result/export', views.redmine_result_export, name='redmine_result_export'),
]
