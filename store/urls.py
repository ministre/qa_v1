from django.urls import path
from . import views


urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:page_id>/', views.item_list, name='item_list'),
    path('all/', views.item_full_list, name='item_full_list'),
    path('all/<int:page_id>/', views.item_full_list, name='item_full_list'),
    path('create/', views.item_create, name='item_create'),
    path('return/<int:item_id>/', views.item_return, name='item_return'),
    path('item/<int:item_id>/', views.item_edit, name='item_edit'),
    path('search/', views.item_search, name='item_search'),
    path('search/<int:page_id>/', views.item_search, name='item_search'),
]
