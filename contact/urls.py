from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactListView.as_view(), name='contacts'),
    path('create/', views.ContactCreate.as_view(), name='contact_create'),
    path('update/<int:pk>/', views.ContactUpdate.as_view(), name='contact_update'),
    path('delete/<int:pk>/', views.ContactDelete.as_view(), name='contact_delete'),
]
