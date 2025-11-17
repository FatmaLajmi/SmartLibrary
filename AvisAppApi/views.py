from django.shortcuts import render

# Create your views here.
# AvisAppApi/views.py
from rest_framework import viewsets
from AvisApp.models import Avis
from .serializers import AvisSerializer
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter

class AvisViewSet(viewsets.ModelViewSet):
    queryset = Avis.objects.all()
    serializer_class = AvisSerializer
    permission_classes = [AllowAny]  # pour tester; changer plus tard
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['date','note']
    search_fields = ['author','book_title']
