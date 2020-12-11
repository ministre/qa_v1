from django.urls import path
from . import views


urlpatterns = [
    path('', views.tcp_udp_check, name='tcp_udp_check'),
]
