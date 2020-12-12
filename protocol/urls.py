from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),
    path('create/', views.ProtocolCreate.as_view(), name='protocol_create'),
    path('update/<int:pk>/', views.ProtocolUpdate.as_view(), name='protocol_update'),
    path('delete/<int:pk>/', views.ProtocolDelete.as_view(), name='protocol_delete'),
    path('<int:pk>/<int:tab_id>/', views.protocol_details, name='protocol_details'),

    path('results/<int:results_id>/', views.protocol_results_edit, name='protocol_results_edit'),
    path('export/<int:protocol_id>/', views.protocol_export, name='protocol_export'),
    path('import/', views.protocol_import, name='protocol_import'),
    path('inherit/<int:protocol_id>/', views.protocol_inherit, name='protocol_inherit'),
]
