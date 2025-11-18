from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UtilisateurRegisterForm
from django.contrib.auth.views import LoginView
from django.urls import reverse

def home(request):
    return render(request, "index.html")

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == "POST":
        form = UtilisateurRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            # Redirect based on role
            if user.role == 'admin':
                return redirect('/admin/')
            return redirect("index")
    else:
        form = UtilisateurRegisterForm()

    return render(request, "UserApp/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "UserApp/login.html"
    authentication_form = None
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # Redirect based on user role
        if self.request.user.role == 'admin':
            return '/admin/'
        return reverse('index')