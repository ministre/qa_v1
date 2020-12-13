from django.urls import path
from . import views


urlpatterns = [
    path('', views.ItemListView.as_view(), name='items'),
    path('create/', views.ItemCreate.as_view(), name='item_create'),
    path('update/<int:pk>/', views.ItemUpdate.as_view(), name='item_update'),
    path('delete/<int:pk>/', views.ItemDelete.as_view(), name='item_delete'),
    path('return/', views.item_return, name='item_return'),
]
