from rest_framework import serializers
from LivreApp.models import Livre
from django.db import transaction

class LivreSerializer(serializers.ModelSerializer):
    # On peut ajouter un champ pour l'upload temporaire si on utilise BLOB
    image_upload = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Livre
        fields = '__all__'
        read_only_fields = ('date_ajout', 'date_modif', 'image_blob')

    @transaction.atomic
    def create(self, validated_data):
        # Récupérer l'image uploadée si présente
        image_file = validated_data.pop('image_upload', None)

        titre = validated_data.get('titre', '').strip()
        auteur = validated_data.get('auteur', '').strip()
        quantite_new = validated_data.get('quantite', 1)

        # Chercher si un livre existant avec même titre et auteur
        existing = Livre.objects.filter(titre__iexact=titre, auteur__iexact=auteur).first()
        if existing:
            existing.quantite += quantite_new
            # Mettre à jour d'autres champs si fournis
            for field in ['isbn', 'date_publication', 'description', 'prix', 'disponible']:
                if field in validated_data and validated_data.get(field) not in (None, ''):
                    setattr(existing, field, validated_data.get(field))
            # Image BLOB
            if image_file:
                existing.image_blob = image_file.read()
            existing.save()
            return existing

        # Sinon créer un nouveau livre
        if image_file:
            validated_data['image_blob'] = image_file.read()
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        # Mettre à jour image si uploadée
        image_file = validated_data.pop('image_upload', None)
        if image_file:
            instance.image_blob = image_file.read()
        return super().update(instance, validated_data)

