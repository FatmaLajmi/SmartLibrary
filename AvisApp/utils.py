# AvisApp/utils.py
from django.db.models import Avg, Count
from .models import Avis
from LivreApp.models import Livre


def get_recommended_books_for_user(user, limit=8):
    """
    Recommandations simples basées sur les avis :
    - Si user non connecté :
        * top livres par moyenne de note globale
    - Si user connecté :
        * on regarde ses genres préférés (avis >= 4)
        * on propose d'autres livres de ces genres, qu'il n'a pas encore notés
        * SI AUCUN RÉSULTAT → on retombe sur le top global
    """
    base_qs = Livre.objects.filter(available=True)

    # 🔹 Cas 1 : user non connecté → top global
    if not user or not user.is_authenticated:
        return (
            base_qs.annotate(
                annotated_average_rating=Avg('avis__note'),
                annotated_reviews_count=Count('avis')
            )
            .order_by('-annotated_average_rating', '-date_added')[:limit]
        )

    # 🔹 Cas 2 : user connecté → on essaie d'abord de personnaliser
    user_genres = (
        Avis.objects.filter(user=user, note__gte=4)
        .values('book_id__genre')
        .annotate(nb=Count('id'))
        .order_by('-nb')
    )
    genres = [g['book_id__genre'] for g in user_genres if g['book_id__genre']]

    qs = base_qs  # fallback = tout le catalogue

    if genres:
        qs_candidate = base_qs.filter(genre__in=genres).exclude(avis__user=user)
        if qs_candidate.exists():
            qs = qs_candidate

    # 🔹 Dans tous les cas, on annote pour trier, mais on ne touche PAS à la propriété `average_rating`
    return (
        qs.annotate(
            annotated_average_rating=Avg('avis__note'),
            annotated_reviews_count=Count('avis')
        )
        .order_by('-annotated_average_rating', '-date_added')[:limit]
    )
