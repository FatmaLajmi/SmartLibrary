# AvisApp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Avis
from LivreApp.models import Livre
from .forms import AvisForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404

class AvisListView(ListView):
    model = Avis
    template_name = 'Avis/list_avis.html'
    context_object_name = 'avis_list'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtrer par livre si book_id est passé en paramètre
        book_id = self.request.GET.get('book_id')
        if book_id:
            qs = qs.filter(book_id=book_id)
        
        # Tri via param ?order=date or ?order=note
        order = self.request.GET.get('order', '-date')
        if order not in ('date', '-date', 'note', '-note'):
            order = '-date'
        return qs.order_by(order)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.request.GET.get('book_id')
        if book_id:
            try:
                context['livre'] = Livre.objects.get(pk=book_id)
            except Livre.DoesNotExist:
                pass
        return context

class AvisCreateView(CreateView):
    model = Avis
    form_class = AvisForm
    template_name = 'Avis/ajouter_avis.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Vérifier que book_id est fourni
        self.book_id = kwargs.get('book_id') or request.GET.get('book_id')
        if not self.book_id:
            messages.error(request, "Aucun livre sélectionné.")
            return redirect('avis_list')
        
        try:
            self.livre = Livre.objects.get(pk=self.book_id)
        except Livre.DoesNotExist:
            raise Http404("Livre non trouvé")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['livre'] = self.livre
        return context
    
    def form_valid(self, form):
        form.instance.book_id = self.livre
        messages.success(self.request, "Avis ajouté avec succès.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('avis_list') + f'?book_id={self.livre.pk}'

class AvisUpdateView(UpdateView):
    model = Avis
    form_class = AvisForm
    template_name = 'Avis/modifier_avis.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['livre'] = self.object.book_id
        return context

    def form_valid(self, form):
        messages.success(self.request, "Avis modifié.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('avis_list') + f'?book_id={self.object.book_id.pk}'

class AvisDeleteView(DeleteView):
    model = Avis
    template_name = 'Avis/supprimer_avis.html'
    
    def get_success_url(self):
        book_id = self.object.book_id.pk
        messages.success(self.request, "Avis supprimé.")
        return reverse_lazy('avis_list') + f'?book_id={book_id}'

class AvisDetailView(DetailView):
    model = Avis
    template_name = 'Avis/detail_avis.html'
    context_object_name = 'avis'