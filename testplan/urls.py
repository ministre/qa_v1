from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanListView.as_view(), name='testplans'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('<int:pk>/<int:tab_id>/', views.testplan_details, name='testplan_details'),
    path('clone/<int:pk>/', views.testplan_clone, name='testplan_clone'),
    path('clear_tests/<int:pk>/', views.clear_tests, name='clear_tests'),

    # categories
    path('category/create/<int:testplan_id>/', views.CategoryCreate.as_view(), name='category_create'),
    path('category/update/<int:pk>/', views.CategoryUpdate.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category_delete'),
    path('category/<int:pk>/<int:tab_id>/', views.category_details, name='category_details'),
    path('category/up/<int:pk>/', views.category_up, name='category_up'),
    path('category/down/<int:pk>/', views.category_down, name='category_down'),

    # tests
    path('test/create/<int:category_id>/', views.TestCreate.as_view(), name='test_create'),
    path('test/update/<int:pk>/', views.TestUpdate.as_view(), name='test_update'),
    path('test/delete/<int:pk>/', views.TestDelete.as_view(), name='test_delete'),
    path('test/<int:pk>/<int:tab_id>/', views.test_details, name='test_details'),
    path('test/up/<int:pk>/', views.test_up, name='test_up'),
    path('test/down/<int:pk>/', views.test_down, name='test_down'),

    # configs
    path('test/config/add/', views.test_config_add, name='test_config_add'),
    path('test/config/create/<int:test_id>/', views.TestConfigCreate.as_view(), name='test_config_create'),
    path('test/config/update/<int:pk>/', views.TestConfigUpdate.as_view(), name='test_config_update'),
    path('test/config/delete/<int:pk>/', views.TestConfigDelete.as_view(), name='test_config_delete'),

    # images
    path('test/image/add/', views.test_image_add, name='test_image_add'),
    path('test/image/create/<int:test_id>/', views.TestImageCreate.as_view(), name='test_image_create'),
    path('test/image/update/<int:pk>/', views.TestImageUpdate.as_view(), name='test_image_update'),
    path('test/image/delete/<int:pk>/', views.TestImageDelete.as_view(), name='test_image_delete'),

    # Testplans Redmine
    path('import/<int:testplan_id>/', views.testplan_import, name='testplan_import'),
    path('test/import/', views.test_import_details, name='test_import_details'),
]
