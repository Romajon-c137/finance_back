"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import path,include
from api.docs import schema_view_v1

# 🎨 КАСТОМИЗАЦИЯ АДМИНКИ - чтобы видеть что production обновлен
admin.site.site_header = "💰 Finance Admin Panel v2.0"
admin.site.site_title = "Finance Admin"
admin.site.index_title = "🚀 Добро пожаловать в панель управления"

urlpatterns = [
    path("api/v1/",include('api.v1.urls')),
    
    # swaggers
    path("api/v1/swagger/", schema_view_v1.with_ui("swagger", cache_timeout=0)),
    
    path('admin/', admin.site.urls),
    path('',lambda r: redirect('admin/')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
