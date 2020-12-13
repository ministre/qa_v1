from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocxTemplateFileListView.as_view(), name='docx_templates'),
    path('template/create/', views.DocxTemplateFileCreate.as_view(), name='docx_template_create'),
    path('template/update/<int:pk>/', views.DocxTemplateFileUpdate.as_view(), name='docx_template_update'),
    path('template/delete/<int:pk>/', views.DocxTemplateFileDelete.as_view(), name='docx_template_delete'),

    path('build/protocol/<int:pk>/', views.build_protocol, name='build_protocol'),
    path('build/protocol_detailed/<int:pk>/', views.build_protocol_detailed, name='build_protocol_detailed'),
    path('build/testplan/<int:pk>/', views.build_testplan, name='build_testplan'),
]
