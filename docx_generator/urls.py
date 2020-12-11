from django.urls import path
from . import views


urlpatterns = [
    path('', views.temp_list, name='temp_list'),
    path('template/create/', views.template_create, name='template_create'),
    path('template/delete/<int:template_id>/', views.template_delete, name='template_delete'),
    path('template/edit/<int:template_id>/', views.template_edit, name='template_edit'),
    path('protocol/create/<int:protocol_id>/', views.create_docx_protocol, name='create_docx_protocol'),
    path('detailed_protocol/create/<int:protocol_id>/', views.create_docx_detailed_protocol,
         name='create_docx_detailed_protocol'),
    path('testplan/create/<int:testplan_id>/', views.create_docx_testplan, name='create_docx_testplan'),
]
