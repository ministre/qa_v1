from django.urls import path
from . import views


urlpatterns = [
    path('build/protocol/', views.build_protocol_beta, name='build_protocol_beta'),
]
