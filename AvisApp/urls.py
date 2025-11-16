from django.urls import path
from . import views

app_name = 'AvisApp'

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('book/<int:book_id>/avis/', views.book_avis_list, name='book_avis_list'),
    path('book/<int:book_id>/avis/ajouter/', views.ajouter_avis, name='ajouter_avis'),
    path('avis/<int:pk>/modifier/', views.modifier_avis, name='modifier_avis'),
    path('avis/<int:pk>/supprimer/', views.supprimer_avis, name='supprimer_avis'),
    path('mes-avis/', views.mes_avis, name='mes_avis'),
]
