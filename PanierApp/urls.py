from django.urls import path
from . import views
from .views import (
    PanierListView,
)

urlpatterns = [
    path('', PanierListView.as_view(), name='panier_list'),
    path('ajouter/<int:livre_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('update-quantite/<int:pk>/', views.update_panier_quantite, name='update_panier_quantite'),
    path('panier/delete/<int:pk>/', views.supprimer_du_panier, name='delete_panier'),
]
