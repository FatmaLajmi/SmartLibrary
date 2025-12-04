from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Livre
from django.db.models import Count
from AvisApp.utils import get_recommended_books_for_user

def index(request):
    """Homepage view with featured books, books by genre, and recommended books"""

    # Featured
    featured_books = (
        Livre.objects.filter(available=True)
        .order_by('-date_added')[:10]
    )

    # Popular by genre
    display_genres = ['fiction', 'mystery', 'romance', 'science_fiction', 'fantasy']

    books_by_genre = {}
    for genre in display_genres:
        genre_books = (
            Livre.objects.filter(
                genre=genre,
                available=True
            )
            .order_by('-date_added')[:8]
        )

        if genre_books.exists():
            books_by_genre[genre] = {
                'name': dict(Livre.GENRE_CHOICES).get(genre, genre.title()),
                'books': genre_books,
            }

    # Recommended
    recommended_books = get_recommended_books_for_user(request.user, limit=8)

    context = {
        'featured_books': featured_books,
        'books_by_genre': books_by_genre,
        'recommended_books': recommended_books,
    }
    return render(request, 'index.html', context)
""" def index(request):
    
    
    # Get 10 most recent books for featured section
    featured_books = Livre.objects.filter(available=True).order_by('-date_added')[:10]
    
    # Define which genres to display (you can customize this list)
    display_genres = ['fiction', 'mystery', 'romance', 'science_fiction', 'fantasy']
    
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
    
    return render(request, 'index.html', context) """


def all_books(request):
    """All books page with pagination and optional genre filter"""
    
    # Get genre filter from URL query params
    genre_filter = request.GET.get('genre', None)
    
    # Base queryset
    books = Livre.objects.filter(available=True).order_by('-date_added')
    
    # Apply genre filter if provided
    if genre_filter and genre_filter in dict(Livre.GENRE_CHOICES):
        books = books.filter(genre=genre_filter)
        selected_genre = dict(Livre.GENRE_CHOICES).get(genre_filter)
    else:
        selected_genre = None
    
    # Pagination - 20 books per page
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all genres that have books (for filter dropdown/buttons)
    available_genres = Livre.objects.filter(available=True).values_list('genre', flat=True).distinct()
    genre_list = [(g, dict(Livre.GENRE_CHOICES).get(g)) for g in available_genres if g]
    
    context = {
        'page_obj': page_obj,
        'books': page_obj.object_list,
        'selected_genre': selected_genre,
        'genre_filter': genre_filter,
        'genre_list': genre_list,
        'total_books': paginator.count,
    }
    
    return render(request, 'all_books.html', context)
