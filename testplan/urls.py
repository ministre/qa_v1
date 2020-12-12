from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanListView.as_view(), name='testplans'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('<int:pk>/<int:tab_id>/', views.testplan_details, name='testplan_details'),


    path('import/<int:testplan_id>/', views.testplan_import, name='testplan_import'),
    path('clear/<int:testplan_id>/', views.clear, name='clear'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('test/delete/<int:test_id>/', views.test_delete, name='test_delete'),
    path('test/import/', views.test_import_details, name='test_import_details'),
]
