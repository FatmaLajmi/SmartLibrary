from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UtilisateurRegisterForm
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == "POST":
        form = UtilisateurRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")  # or your chosen view
    else:
        form = UtilisateurRegisterForm()

    return render(request, "UserApp/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "UserApp/login.html"
    authentication_form = None  # Django will generate the right form automatically
    redirect_authenticated_user = True