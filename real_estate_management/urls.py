"""
URL configuration for real_estate_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from api.views import LoginView,PropertyListCreateView, PropertyDetailView,UnitListView, UnitListCreateView, UnitDetailView, TenantListCreateView, TenantDetailView,PropertySearchAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/',LoginView.as_view(),name='login'),
    path('api/properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('api/properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('api/units/', UnitListCreateView.as_view(), name='unit-list'),
    path('api/properties/<int:property_id>/units/', UnitListView.as_view(), name='unit-list'),
    path('api/units/<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('api/tenants/', TenantListCreateView.as_view(), name='tenant-list'),
    path('api/tenants/<int:pk>/', TenantDetailView.as_view(), name='tenant-detail'),
    path('api/property_search/', PropertySearchAPIView.as_view(), name='property_search_api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

