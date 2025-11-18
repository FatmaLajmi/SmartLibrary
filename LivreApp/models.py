import base64
from django.db import models
from django.utils.html import format_html


class Livre(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    image_blob = models.BinaryField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('fantasy', 'Fantasy'),
        ('science_fiction', 'Science Fiction'),
        ('mystery', 'Mystery'),
        ('thriller', 'Thriller'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('historical', 'Historical'),
        ('biography', 'Biography'),
        ('autobiography', 'Autobiography'),
        ('self_help', 'Self-Help'),
        ('poetry', 'Poetry'),
        ('young_adult', 'Young Adult'),
        ('children', 'Children'),
        ('classics', 'Classics'),
        ('graphic_novel', 'Graphic Novel'),
        ('crime', 'Crime'),
        ('adventure', 'Adventure'),
        ('drama', 'Drama'),
        ('philosophy', 'Philosophy'),
        ('education', 'Education'),
        ('business', 'Business'),
        ('religion', 'Religion'),
        ('travel', 'Travel'),
        ('art', 'Art'),
        ('cookbook', 'Cookbook'),
        ('health', 'Health'),
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True, null=True)

    def image_tag(self):
        """Display image preview in admin"""
        if self.image_blob:
            b64 = base64.b64encode(self.image_blob).decode()
            return format_html(
                '<img src="data:image/jpeg;base64,{}" width="60" height="80" '
                'style="object-fit: cover; border-radius:4px;" />',
                b64
            )
        return "—"
    image_tag.short_description = "Preview"

    def __str__(self):
        return f"{self.title} — {self.author}"

    class Meta:
        ordering = ['-date_added']
        verbose_name = "Book"
        verbose_name_plural = "Books"
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', 'isbn'],
                name='unique_book_combination'
            )
        ]
