from django.urls import path
from .views import (
    LivreListView, LivreDetailView, LivreCreateView, LivreUpdateView, LivreDeleteView
)

urlpatterns = [
    path('', LivreListView.as_view(), name='livre_list'),           # liste
    path('add/', LivreCreateView.as_view(), name='livre_create'),   # ajouter
    path('<int:pk>/', LivreDetailView.as_view(), name='livre_detail'), 
    path('<int:pk>/edit/', LivreUpdateView.as_view(), name='livre_update'),
    path('<int:pk>/delete/', LivreDeleteView.as_view(), name='livre_delete'),
]

