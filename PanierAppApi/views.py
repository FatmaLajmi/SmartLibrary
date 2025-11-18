from rest_framework import viewsets, filters
from PanierApp.models import Panier
from .serializers import PanierSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre']
    ordering_fields = ['prix', 'quantite']
    parser_classes = [JSONParser, FormParser, MultiPartParser]
