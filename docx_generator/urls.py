from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocxTemplateFileListView.as_view(), name='docx_templates'),
    path('template/create/', views.DocxTemplateFileCreate.as_view(), name='docx_template_create'),
    path('template/update/<int:pk>/', views.DocxTemplateFileUpdate.as_view(), name='docx_template_update'),
    path('template/delete/<int:pk>/', views.DocxTemplateFileDelete.as_view(), name='docx_template_delete'),

    path('build_protocol/<int:pk>/', views.create_docx_protocol, name='create_docx_protocol'),
    path('build_detailed_protocol/<int:pk>/', views.create_docx_detailed_protocol, name='create_docx_detailed_protocol'),
    path('testplan/create/<int:testplan_id>/', views.create_docx_testplan, name='create_docx_testplan'),
]
