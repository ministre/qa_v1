from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocxTemplateListView.as_view(), name='docx_templates'),
    path('template/create/', views.DocxTemplateCreate.as_view(), name='docx_template_create'),
    path('template/delete/<int:template_id>/', views.template_delete, name='template_delete'),
    path('template/edit/<int:template_id>/', views.template_edit, name='template_edit'),
    path('build_protocol/<int:pk>/', views.create_docx_protocol, name='create_docx_protocol'),
    path('build_detailed_protocol/<int:pk>/', views.create_docx_detailed_protocol, name='create_docx_detailed_protocol'),
    path('testplan/create/<int:testplan_id>/', views.create_docx_testplan, name='create_docx_testplan'),
]
