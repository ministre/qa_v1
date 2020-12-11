from django.urls import path
from . import views

urlpatterns = [
    path('', views.shipment_list, name='shipment_list'),
    path('<int:shipment_id>/', views.shipment_create_report, name='shipment_create_report'),
]
