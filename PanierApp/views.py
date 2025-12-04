from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Panier
from LivreApp.models import Livre

class PanierListView(ListView):
    template_name = 'Panier/cart_list.html'
    context_object_name = 'panier_list'

    def get_queryset(self):
        qs = Panier.objects.filter(user=self.request.user)
        # Tri selon paramètre GET "sort": price_asc ou price_desc
        sort = self.request.GET.get('sort', '')
        if sort == 'price_asc':
            qs = qs.order_by('prix')
        elif sort == 'price_desc':
            qs = qs.order_by('-prix')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.get_queryset()
        context['total'] = sum(item.prix_total for item in items)
        context['current_sort'] = self.request.GET.get('sort', '')
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
