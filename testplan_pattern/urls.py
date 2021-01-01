from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanPatternListView.as_view(), name='testplan_patterns'),
    path('create/', views.TestplanPatternCreate.as_view(), name='testplan_pattern_create'),
    path('update/<int:pk>/', views.TestplanPatternUpdate.as_view(), name='testplan_pattern_update'),
    path('delete/<int:pk>/', views.TestplanPatternDelete.as_view(), name='testplan_pattern_delete'),
    path('<int:pk>/<int:tab_id>/', views.testplan_pattern_details, name='testplan_pattern_details'),
    # categories
    path('category/create/<int:testplan_id>/', views.CategoryPatternCreate.as_view(), name='category_pattern_create'),
    # path('category/update/<int:pk>/', views.CategoryPatternUpdate.as_view(), name='category_pattern_update'),
    # path('category/delete/<int:pk>/', views.CategoryPatternDelete.as_view(), name='category_pattern_delete'),
    # path('category/<int:pk>/<int:tab_id>/', views.category_pattern_details, name='category_pattern_details'),
]
