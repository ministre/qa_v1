from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanPatternListView.as_view(), name='testplan_patterns'),
    path('create/', views.TestplanPatternCreate.as_view(), name='testplan_pattern_create'),
    path('update/<int:pk>/', views.TestplanPatternUpdate.as_view(), name='testplan_pattern_update'),
    path('delete/<int:pk>/', views.TestplanPatternDelete.as_view(), name='testplan_pattern_delete'),
    path('<int:pk>/<int:tab_id>/', views.testplan_pattern_details, name='testplan_pattern_details'),
]
