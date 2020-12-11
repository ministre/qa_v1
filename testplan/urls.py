from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanListView.as_view(), name='testplans'),

    path('create/', views.testplan_create, name='testplan_create'),
    path('delete/<int:testplan_id>/', views.testplan_delete, name='testplan_delete'),
    path('edit/<int:testplan_id>/', views.testplan_edit, name='testplan_edit'),
    path('<int:pk>/', views.testplan_details, name='testplan_details'),
    path('import/<int:testplan_id>/', views.testplan_import, name='testplan_import'),
    path('clear/<int:testplan_id>/', views.clear, name='clear'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('test/delete/<int:test_id>/', views.test_delete, name='test_delete'),
    path('test/import/', views.test_import_details, name='test_import_details'),
]
