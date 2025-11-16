# AvisAppApi/urls.py
from rest_framework.routers import DefaultRouter
from .views import AvisViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', AvisViewSet, basename='api-avis')

urlpatterns = [
    path('', include(router.urls)),
]
