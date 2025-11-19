from django.shortcuts import render
from LivreApp.models import Livre

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
    
    return render(request, 'index.html', context)
