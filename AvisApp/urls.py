# AvisApp/urls.py
from django.urls import path
from .views import (
    AvisListView, AvisCreateView, AvisUpdateView, AvisDeleteView, AvisDetailView
)

urlpatterns = [
    path('', AvisListView.as_view(), name='avis_list'),
    path('ajouter/<int:book_id>/', AvisCreateView.as_view(), name='ajouter_avis'),
    path('modifier/<int:pk>/', AvisUpdateView.as_view(), name='modifier_avis'),
    path('supprimer/<int:pk>/', AvisDeleteView.as_view(), name='supprimer_avis'),
    path('detail/<int:pk>/', AvisDetailView.as_view(), name='detail_avis'),
]