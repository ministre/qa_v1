from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),
    path('create/', views.ProtocolCreate.as_view(), name='protocol_create'),

    #path('create/', views.protocol_create, name='protocol_create'),

    path('<int:pk>/', views.protocol_show, name='protocol_show'),
    path('delete/<int:protocol_id>/', views.protocol_delete, name='protocol_delete'),
    path('edit/<int:protocol_id>/', views.protocol_edit, name='protocol_edit'),
    path('results/<int:results_id>/', views.protocol_results_edit, name='protocol_results_edit'),
    path('export/<int:protocol_id>/', views.protocol_export, name='protocol_export'),
    path('import/', views.protocol_import, name='protocol_import'),
    path('inherit/<int:protocol_id>/', views.protocol_inherit, name='protocol_inherit'),
]
