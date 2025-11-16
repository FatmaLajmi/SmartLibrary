from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Book, Avis
from .forms import AvisForm
from django.db.models import Avg, Count
def parse_sort_param(request):
    # renvoie tuple (order_by_field, friendly_label)
    s = request.GET.get('sort', 'date_desc')
    if s == 'date_asc':
        return ('date', 'Date ↑')
    if s == 'date_desc':
        return ('-date', 'Date ↓')
    if s == 'note_asc':
        return ('note', 'Note ↑')
    if s == 'note_desc':
        return ('-note', 'Note ↓')
    return ('-date', 'Date ↓')

def book_avis_list(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    order_by, sort_label = parse_sort_param(request)
    avis_qs = book.avis.all().order_by(order_by)
    # pagination simple
    paginator = Paginator(avis_qs, 10)
    page = request.GET.get('page')
    avis_page = paginator.get_page(page)
    return render(request, 'Avis/book_avis_list.html', {
        'book': book,
        'avis_page': avis_page,
        'sort_label': sort_label,
    })

@login_required
def ajouter_avis(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            avis.user = request.user
            avis.book = book  # 🔒 on force le book depuis l’URL
            avis.save()
            return redirect('AvisApp:book_avis_list', book_id=book.id)
    else:
        form = AvisForm(initial={'book': book})
        # 🔒 on désactive le champ “book” pour ne pas pouvoir le modifier
        form.fields['book'].disabled = True
    return render(request, 'Avis/avis_form.html', {'form': form, 'book': book, 'action': 'Ajouter'})


@login_required
def modifier_avis(request, pk):
    avis = get_object_or_404(Avis, pk=pk)
    if avis.user != request.user:
        return HttpResponseForbidden("Tu ne peux modifier que tes propres avis.")
    if request.method == 'POST':
        form = AvisForm(request.POST, instance=avis)
        if form.is_valid():
            form.save()
            return redirect('AvisApp:mes_avis')
    else:
        form = AvisForm(instance=avis)
    return render(request, 'Avis/avis_form.html', {'form': form, 'book': avis.book, 'action': 'Modifier'})

@login_required
def supprimer_avis(request, pk):
    avis = get_object_or_404(Avis, pk=pk)
    if avis.user != request.user:
        return HttpResponseForbidden("Tu ne peux supprimer que tes propres avis.")
    if request.method == 'POST':
        book_id = avis.book.id
        avis.delete()
        # redirection vers la page des avis du livre
        return redirect('AvisApp:book_avis_list', book_id=book_id)
    return render(request, 'Avis/avis_confirm_delete.html', {'avis': avis})

@login_required
def mes_avis(request):
    order_by, sort_label = parse_sort_param(request)
    qs = Avis.objects.filter(user=request.user).order_by(order_by)
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    avis_page = paginator.get_page(page)
    return render(request, 'Avis/mes_avis.html', {
        'avis_page': avis_page,
        'sort_label': sort_label,
    })
def book_list(request):
    """Affiche la liste des livres avec leur moyenne de notes"""
    books = (
        Book.objects
        .annotate(
            moyenne_note=Avg('avis__note'),
            total_avis=Count('avis')
        )
        .order_by('title')
    )
    return render(request, 'Avis/book_list.html', {'books': books})