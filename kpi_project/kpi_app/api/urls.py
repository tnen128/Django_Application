# kpi_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KPIViewSet, AssetViewSet, AssetKPIViewSet

# Factory Pattern: using a router to create and register viewsets.
router = DefaultRouter()
router.register(r'kpis', KPIViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'asset-kpis', AssetKPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
