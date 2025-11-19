from django.urls import path
from . import views
from .views import (
    PanierListView,
    PanierCreateView,
    PanierUpdateView,
    PanierDeleteView,
)

urlpatterns = [
    path('', PanierListView.as_view(), name='panier_list'),
    path('ajouter/<int:livre_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('create/', PanierCreateView.as_view(), name='create_panier'),
    path('update-quantite/<int:pk>/', views.update_panier_quantite, name='update_panier_quantite'),
    path('<int:pk>/update/', PanierUpdateView.as_view(), name='update_panier'),
    path('<int:pk>/delete/', PanierDeleteView.as_view(), name='delete_panier'),
]
