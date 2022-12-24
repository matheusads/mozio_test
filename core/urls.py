"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from core.api import views
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ServiceArea API",
        default_version='v1',
        description=
        "A API for retrieving user providers working in areas from coordinates.",
        contact=openapi.Contact(email="matheusamorimsouza@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('providers/', views.ProviderView.as_view(), name='providers'),
    path('providers/<uuid:pk>/',
         views.ProviderDetails.as_view(),
         name='providers_details'),
    path('service_areas/',
         views.ServiceAreaView.as_view(),
         name='service_areas_views'),
    path('service_areas/<uuid:pk>/',
         views.ServiceAreaDetails.as_view(),
         name='service_areas_details'),
    path('get_areas/', views.ServiceAreaAPI.as_view(), name='providers'),
]
urlpatterns += [
    re_path('docs(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path('docs/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path('redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
