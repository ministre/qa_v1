from django.urls import path
from . import views


urlpatterns = [
    path('', views.sip_invite, name='sip_invite'),
]
