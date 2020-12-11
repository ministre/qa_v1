from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocol_list, name='protocol_list'),
    path('<int:protocol_id>/', views.protocol_show, name='protocol_show'),
    path('create/', views.protocol_create, name='protocol_create'),
    path('delete/<int:protocol_id>/', views.protocol_delete, name='protocol_delete'),
    path('edit/<int:protocol_id>/', views.protocol_edit, name='protocol_edit'),
    path('results/<int:results_id>/', views.protocol_results_edit, name='protocol_results_edit'),
    path('export/<int:protocol_id>/', views.protocol_export, name='protocol_export'),
    path('import/', views.protocol_import, name='protocol_import'),
    path('inherit/<int:protocol_id>/', views.protocol_inherit, name='protocol_inherit'),
]
