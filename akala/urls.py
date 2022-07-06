"""akala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from . import settings
from django.views.static import serve

urlpatterns = [
    path("", include("food.urls")),
    path("c/", include("company.urls")),
    #url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    #url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    url("media/(?P<path>.*)", serve,
        {"document_root": settings.MEDIA_ROOT}),
    url("static/(?P<path>.*)", serve,
        {"document_root": settings.STATIC_ROOT}),
    path("apis/", include('apis.urls')),
    path('api-auth/', include("rest_framework.urls")),
]
