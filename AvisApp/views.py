# AvisApp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Avis
from .forms import AvisForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View

class AvisListView(ListView):
    model = Avis
    template_name = 'Avis/list_avis.html'
    context_object_name = 'avis_list'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        # tri via param ?order=date or ?order=note (prefix - pour desc)
        order = self.request.GET.get('order', 'date')  # default par date
        if order not in ('date','-date','note','-note'):
            order = 'date'
        return qs.order_by(order)

class AvisCreateView(CreateView):
    model = Avis
    form_class = AvisForm
    template_name = 'Avis/ajouter_avis.html'
    success_url = reverse_lazy('avis_list')

    def form_valid(self, form):
        messages.success(self.request, "Avis ajouté avec succès.")
        return super().form_valid(form)

class AvisUpdateView(UpdateView):
    model = Avis
    form_class = AvisForm
    template_name = 'Avis/modifier_avis.html'
    success_url = reverse_lazy('avis_list')

    def form_valid(self, form):
        messages.success(self.request, "Avis modifié.")
        return super().form_valid(form)

class AvisDeleteView(DeleteView):
    model = Avis
    template_name = 'Avis/supprimer_avis.html'
    success_url = reverse_lazy('avis_list')

class AvisDetailView(DetailView):
    model = Avis
    template_name = 'Avis/detail_avis.html'
    context_object_name = 'avis'
class MesAvisView(ListView):
    model = Avis
    template_name = 'Avis/mes_avis.html'
    context_object_name = 'mes_avis'
    paginate_by = 5

    def get_queryset(self):
        # On récupère un param author passé en GET pour simuler l'user: ?author=Eya
        author = self.request.GET.get('author', '')
        qs = Avis.objects.filter(author=author).order_by('-date')
        return qs