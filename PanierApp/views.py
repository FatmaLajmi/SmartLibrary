from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Panier
from .forms import PanierForm  # formulaire adapté à Panier

# ----------------------------------------------------
# 🧾 Vue fonctionnelle pour lister le panier
# ----------------------------------------------------
def panier_liste(request):
    """
    Affiche tous les éléments du panier et le total.
    """
    items = Panier.objects.all()  # pour l'instant tous les éléments, plus tard filtrer par utilisateur
    total = sum(item.prix_total() for item in items)
    return render(request, 'Panier/cart_list.html', {'panier_list': items, 'total': total})


# ----------------------------------------------------
# 📋 Class-based ListView
# ----------------------------------------------------
class PanierListView(ListView):
    model = Panier
    template_name = 'Panier/cart_list.html'
    context_object_name = 'panier_list'
    ordering = ['titre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pour l'instant tous les éléments, plus tard filtrer par utilisateur connecté
        items = Panier.objects.all()
        context['total'] = sum(item.prix_total() for item in items)
        return context


# ----------------------------------------------------
# ➕ CreateView
# ----------------------------------------------------
class PanierCreateView(CreateView):
    model = Panier
    template_name = 'Panier/cart_form.html'
    form_class = PanierForm
    success_url = reverse_lazy('panier_list')

    def form_valid(self, form):
        # ici tu peux ajouter un utilisateur par défaut si nécessaire
        # form.instance.utilisateur = self.request.user
        return super().form_valid(form)


# ----------------------------------------------------
# ✏️ UpdateView
# ----------------------------------------------------
class PanierUpdateView(UpdateView):
    model = Panier
    template_name = 'Panier/cart_form.html'
    form_class = PanierForm
    success_url = reverse_lazy('panier_list')


# ----------------------------------------------------
# ❌ DeleteView
# ----------------------------------------------------
class PanierDeleteView(DeleteView):
    model = Panier
    template_name = 'Panier/cart_confirm_delete.html'
    success_url = reverse_lazy('panier_list')


# ----------------------------------------------------
# ➕ Ajouter un livre directement depuis le catalogue
# ----------------------------------------------------
def ajouter_au_panier(request, title=None, prix=None):
    """
    Ajoute un livre au panier directement, sans formulaire.
    title et prix peuvent être passés depuis le catalogue.
    """
    if not title or not prix:
        # valeurs par défaut pour test / placeholder
        title = "Livre Exemple"
        prix = 12.5

    # Vérifie si le livre est déjà dans le panier
    item, created = Panier.objects.get_or_create(
        title=title,
        prix=prix,
    )

    if not created:
        # incrémente la quantité si déjà présent
        item.quantite += 1
        item.save()

    return redirect('panier_list')
