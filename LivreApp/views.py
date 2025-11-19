from django.shortcuts import render
from .models import Livre
import base64

def index(request):
    livres = Livre.objects.all()
    return render(request, 'index.html', {'livres': livres})

