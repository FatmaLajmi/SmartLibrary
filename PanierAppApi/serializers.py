from PanierApp.models import Panier
from rest_framework import serializers

class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = '__all__'
