# AvisApp/utils.py
from django.db.models import Avg, Count
from .models import Avis
from LivreApp.models import Livre


def get_recommended_books_for_user(user, limit=8):
    """
    Recommandations simples basées sur les avis :
    - Si user connecté :
        * on regarde les genres où il a mis des bonnes notes (>=4)
        * on propose d'autres livres du même genre, qu'il n'a pas encore notés
        * triés par meilleure moyenne de note globale + date ajout
    - Si user non connecté :
        * top livres par moyenne de note
    """
    qs = Livre.objects.filter(available=True)

    # Pas connecté -> recommandations globales
    if not user.is_authenticated:
        return qs.annotate(avg_note=Avg('avis__note')).order_by('-avg_note', '-date_added')[:limit]

    # Genres préférés du user (où il met 4 ou 5)
    user_genres = (
        Avis.objects.filter(user=user, note__gte=4)
        .values('book_id__genre')
        .annotate(nb=Count('id'))
        .order_by('-nb')
    )

    genres = [g['book_id__genre'] for g in user_genres if g['book_id__genre']]

    if genres:
        qs = qs.filter(genre__in=genres)
        # on évite de proposer des livres qu'il a déjà notés
        qs = qs.exclude(avis__user=user)

    # si aucun genre préféré ou aucun résultat, on retombe sur top global
    qs = qs.annotate(avg_note=Avg('avis__note')).order_by('-avg_note', '-date_added')
    return qs[:limit]
