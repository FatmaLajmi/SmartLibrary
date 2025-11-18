from django.urls import path
from .views import (
    PanierListView,
    PanierCreateView,
    PanierUpdateView,
    PanierDeleteView,
)

urlpatterns = [
    path('', PanierListView.as_view(), name='panier_list'),
    path('create/', PanierCreateView.as_view(), name='create_panier'),
    path('<int:pk>/update/', PanierUpdateView.as_view(), name='update_panier'),
    path('<int:pk>/delete/', PanierDeleteView.as_view(), name='delete_panier'),
]
