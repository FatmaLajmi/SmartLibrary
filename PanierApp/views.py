from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Panier
from LivreApp.models import Livre
from .forms import PanierForm
from django.shortcuts import get_object_or_404



# -------------------------------------------
# 📌 LISTE PANIER
# -------------------------------------------
import base64

def panier_liste(request):
    items = Panier.objects.all()
    total = sum(item.prix_total() for item in items)  # Note les parenthèses !

    return render(request, 'Panier/cart_list.html', {'panier_list': items, 'total': total})




class PanierListView(ListView):
    model = Panier
    template_name = 'Panier/cart_list.html'
    context_object_name = 'panier_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Panier.objects.all()
        context['total'] = sum(item.prix_total for item in items)
        return context


# -------------------------------------------
# 📌 AJOUTER via formulaire Django
# -------------------------------------------
class PanierCreateView(CreateView):
    model = Panier
    template_name = 'Panier/cart_form.html'
    form_class = PanierForm
    success_url = reverse_lazy('panier_list')


class PanierUpdateView(UpdateView):
    model = Panier
    template_name = 'Panier/cart_form.html'
    form_class = PanierForm
    success_url = reverse_lazy('panier_list')

def update_panier_quantite(request, pk):
    item = get_object_or_404(Panier, pk=pk)
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        item.quantite = quantite
        item.save()
    return redirect('panier_list')


class PanierDeleteView(DeleteView):
    model = Panier
    template_name = 'Panier/cart_confirm_delete.html'
    success_url = reverse_lazy('panier_list')


# -------------------------------------------
# 📌 AJOUTER UN LIVRE DEPUIS LE CATALOGUE
# -------------------------------------------
def ajouter_au_panier(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)

    item, created = Panier.objects.get_or_create(
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

