from rest_framework import viewsets, filters
from LivreApp.models import Livre
from .serializers import LivreSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    parser_classes = (MultiPartParser, FormParser)  # allows image upload via multipart/form-data
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'isbn', 'description']
    ordering_fields = ['date_added', 'title', 'author']
