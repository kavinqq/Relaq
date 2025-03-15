"""
URL configuration for relaq project.

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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Relaq API",
        default_version='v1',
        description="Relaq API 文件",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="isu101220@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), 
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 應用 URL
    path('', include('cms.urls')),
]

# 在開發環境中提供媒體文件
if settings.DEBUG:    
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    
    urlpatterns += [
        # Swagger 文檔 URL - 使用自定義路徑
        re_path(r'^api-schema(?P<format>\.json|\.yaml)/$', schema_view.without_ui(cache_timeout=0), name='schema-json-yaml'),
        path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('api-redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]


# admin settings
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE