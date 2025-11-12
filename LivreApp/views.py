from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Livre
from .forms import LivreForm

# Create your views here.

class LivreListView(ListView):
    model = Livre
    template_name = 'livre/livre_list.html'
    context_object_name = 'livres'

class LivreDetailView(DetailView):
    model = Livre
    template_name = 'livre/livre_detail.html'

class LivreCreateView(CreateView):
    model = Livre
    form_class = LivreForm
    template_name = 'livre/livre_form.html'
    success_url = reverse_lazy('livre_list')

    # On veut la logique "si même titre+auteur => augmenter la quantité" aussi côté form
    def form_valid(self, form):
        titre = form.cleaned_data.get('titre', '').strip()
        auteur = form.cleaned_data.get('auteur', '').strip()
        quantite_new = form.cleaned_data.get('quantite', 1)
        existing = Livre.objects.filter(titre__iexact=titre, auteur__iexact=auteur).first()
        if existing:
            existing.quantite = existing.quantite + quantite_new
            # mettre à jour champs si fournis
            for field in ['isbn', 'date_publication', 'image', 'description', 'prix', 'disponible']:
                val = form.cleaned_data.get(field)
                if val not in (None, ''):
                    setattr(existing, field, val)
            existing.save()
            return super().form_valid(form)  # redirige (même si on a mis à jour l'existant)
        return super().form_valid(form)

class LivreUpdateView(UpdateView):
    model = Livre
    form_class = LivreForm
    template_name = 'livre/livre_form.html'
    success_url = reverse_lazy('livre_list')

class LivreDeleteView(DeleteView):
    model = Livre
    template_name = 'livre/livre_confirm_delete.html'
    success_url = reverse_lazy('livre_list')
