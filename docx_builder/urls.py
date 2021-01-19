from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocxProfileListView.as_view(), name='docx_profiles'),
    path('profile/create/', views.DocxProfileCreate.as_view(), name='docx_profile_create'),
    path('profile/update/<int:pk>/', views.DocxProfileUpdate.as_view(), name='docx_profile_update'),
    path('profile/delete/<int:pk>/', views.DocxProfileDelete.as_view(), name='docx_profile_delete'),
    path('build/protocol/', views.build_protocol_beta, name='build_protocol_beta'),
]
