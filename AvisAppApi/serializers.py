# AvisAppApi/serializers.py
from rest_framework import serializers
from AvisApp.models import Avis

class AvisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avis
        fields = ['id','book_title','author','note','commentaire','date']
