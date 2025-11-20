from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Panier
from LivreApp.models import Livre

class PanierListView(ListView):
    template_name = 'Panier/cart_list.html'
    context_object_name = 'panier_list'

    def get_queryset(self):
        return Panier.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Panier.objects.filter(user=self.request.user)
        context['total'] = sum(item.prix_total for item in items)
        return context
    

def ajouter_au_panier(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)

    item, created = Panier.objects.get_or_create(
        user=request.user,
        livre=livre,
        defaults={
            'titre': livre.title,
            'prix': livre.price,
            'quantite': 1
        }
    )

    if not created:
        item.quantite += 1
        item.save()

    return redirect('panier_list')


def update_panier_quantite(request, pk):
    item = get_object_or_404(Panier, pk=pk, user=request.user)
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        item.quantite = quantite
        item.save()
    return redirect('panier_list')


def supprimer_du_panier(request, pk):
    item = get_object_or_404(Panier, pk=pk, user=request.user)
    item.delete()
    return redirect('panier_list')
