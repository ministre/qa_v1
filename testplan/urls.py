from django.urls import path
from . import views

urlpatterns = [
    # Testplans
    path('', views.TestplanListView.as_view(), name='testplans'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('<int:pk>/<int:tab_id>/', views.testplan_details, name='testplan_details'),
    path('clone/<int:pk>/', views.testplan_clone, name='testplan_clone'),
    path('clear_tests/<int:tp_id>/', views.clear_tests, name='clear_tests'),
    # Testplans Redmine
    path('import/<int:testplan_id>/', views.testplan_import, name='testplan_import'),
    # Tests
    path('test/create/<int:tp_id>/', views.TestCreate.as_view(), name='test_create'),
    path('test/update/<int:pk>/', views.TestUpdate.as_view(), name='test_update'),
    path('test/delete/<int:pk>/', views.TestDelete.as_view(), name='test_delete'),

    path('test/<int:pk>/<int:tab_id>', views.test_details, name='test_details'),


    path('test/import/', views.test_import_details, name='test_import_details'),
]
