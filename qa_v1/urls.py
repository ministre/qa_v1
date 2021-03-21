"""qa_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('i18n/setlang', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('device.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('contact/', include('contact.urls')),
    path('device/', include('device.urls')),
    path('docx_builder/', include('docx_builder.urls')),
    path('docx/', include('docx_generator.urls')),
    path('protocol/', include('protocol.urls')),
    path('redmine/', include('redmine.urls')),
    path('shipment/', include('shipment.urls')),
    path('sip_invite/', include('sip_invite.urls')),
    path('store/', include('store.urls')),
    path('tech_req/', include('tech_req.urls')),
    path('tcp_udp_check/', include('tcp_udp_check.urls')),
    path('testplan/', include('testplan.urls')),
    path('testplan_pattern/', include('testplan_pattern.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
