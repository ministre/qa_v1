from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanPatternListView.as_view(), name='testplan_patterns'),
    path('create/', views.TestplanPatternCreate.as_view(), name='testplan_pattern_create'),
    path('update/<int:pk>/', views.TestplanPatternUpdate.as_view(), name='testplan_pattern_update'),
    path('delete/<int:pk>/', views.TestplanPatternDelete.as_view(), name='testplan_pattern_delete'),
    path('<int:pk>/<int:tab_id>/', views.testplan_pattern_details, name='testplan_pattern_details'),
    path('category/create/<int:testplan_pattern_id>/', views.CategoryPatternCreate.as_view(),
         name='category_pattern_create'),
    path('category/update/<int:pk>/', views.CategoryPatternUpdate.as_view(), name='category_pattern_update'),
    path('category/delete/<int:pk>/', views.CategoryPatternDelete.as_view(), name='category_pattern_delete'),
    path('category/<int:pk>/<int:tab_id>/', views.category_pattern_details, name='category_pattern_details'),
    path('category/up/<int:pk>/', views.category_pattern_up, name='category_pattern_up'),
    path('category/down/<int:pk>/', views.category_pattern_down, name='category_pattern_down'),
    path('test/create/<int:category_pattern_id>/', views.TestPatternCreate.as_view(), name='test_pattern_create'),
    path('test/update/<int:pk>/', views.TestPatternUpdate.as_view(), name='test_pattern_update'),
    path('test/delete/<int:pk>/', views.TestPatternDelete.as_view(), name='test_pattern_delete'),
    path('test/<int:pk>/<int:tab_id>/', views.test_pattern_details, name='test_pattern_details'),
    path('test/up/<int:pk>/', views.test_pattern_up, name='test_pattern_up'),
    path('test/down/<int:pk>/', views.test_pattern_down, name='test_pattern_down'),
    path('test_names_update/', views.test_names_update, name='test_names_update'),
    path('test_purposes_update/', views.test_purposes_update, name='test_purposes_update'),
    path('test_procedures_update/', views.test_procedures_update, name='test_procedures_update'),
    path('test_expected_update/', views.test_expected_update, name='test_expected_update'),
]
