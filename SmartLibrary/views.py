from django.shortcuts import render
from LivreApp.models import Livre
<<<<<<< HEAD
from AvisApp.utils import get_recommended_books_for_user  
=======
from django.db.models import Q
from django.core.paginator import Paginator



>>>>>>> main
def index(request):
    """Homepage view with featured books and books by genre"""
    
    # Get 10 most recent books for featured section
    featured_books = Livre.objects.filter(available=True).order_by('-date_added')[:10]
    
    # Define which genres to display (you can customize this list)
    display_genres = ['fiction', 'mystery', 'romance', 'science_fiction', 'fantasy','children','horror']
    
    # Get books by genre (2 rows of 4 = 8 books per genre)
    books_by_genre = {}
    for genre in display_genres:
        genre_books = Livre.objects.filter(
            genre=genre, 
            available=True
        ).order_by('-date_added')[:8]
        
        if genre_books.exists():
            books_by_genre[genre] = {
                'name': dict(Livre.GENRE_CHOICES).get(genre, genre.title()),
                'books': genre_books
            }
    
    context = {
        'featured_books': featured_books,
        'books_by_genre': books_by_genre,
    }
    recommended_books = get_recommended_books_for_user(request.user)

    context = {
        'featured_books': featured_books,
        'books_by_genre': books_by_genre,
        'recommended_books': recommended_books,   # 🔴 AJOUT
    }
    return render(request, 'index.html', context)


def all_books(request):
    # --- RÉCUPÉRATION DES FILTRES ---
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')

    # --- LISTE DES LIVRES ---
    books = Livre.objects.all()

    # --- FILTRE RECHERCHE ---
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    # --- FILTRE GENRE ---
    if genre_filter:
        books = books.filter(genre=genre_filter)

    # --- PAGINATION ---
    paginator = Paginator(books, 12)  # 12 livres par page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # --- LISTE DE GENRES (clé + nom affiché) ---
    genre_list = Livre.GENRE_CHOICES  # si tu as un CHOICES dans le modèle

    # --- COMPTE ---
    total_books = books.count()

    context = {
        "books": page_obj,
        "page_obj": page_obj,
        "total_books": total_books,
        "genre_list": genre_list,
        "genre_filter": genre_filter,
        "selected_genre": dict(genre_list).get(genre_filter),
        "request": request,
    }

    return render(request, "all_books.html", context)

