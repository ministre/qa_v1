from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),
    path('create/', views.ProtocolCreate.as_view(), name='protocol_create'),
    path('update/<int:pk>/', views.ProtocolUpdate.as_view(), name='protocol_update'),
    path('delete/<int:pk>/', views.ProtocolDelete.as_view(), name='protocol_delete'),
    path('<int:pk>/<int:tab_id>/', views.protocol_details, name='protocol_details'),
    path('test_result/update/<int:pk>/', views.TestResultUpdate.as_view(), name='test_result_update'),
    path('import/', views.protocol_import, name='protocol_import'),
    path('copy_results/', views.protocol_copy_results, name='protocol_copy_results'),
]
