from rest_framework import serializers
from LivreApp.models import Livre
from django.db import transaction

class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = '__all__'
        read_only_fields = ('date_ajout', 'date_modif')

    def validate_isbn(self, value):
        # Permettre isbn vide, sinon s'assurer d'unicité
        if value in (None, ''):
            return value
        qs = Livre.objects.filter(isbn=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ce ISBN est déjà utilisé.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        # Si titre ET auteur existent -> on augmente la quantité
        titre = validated_data.get('titre', '').strip()
        auteur = validated_data.get('auteur', '').strip()
        quantite_new = validated_data.get('quantite', 1)

        existing = Livre.objects.filter(titre__iexact=titre, auteur__iexact=auteur).first()
        if existing:
            # Si IL EXISTE, incrémente la quantité et met à jour autres champs éventuellement fournis
            existing.quantite = existing.quantite + quantite_new
            # Mettre à jour éventuellement image/description/prix si fournis
            for field in ['isbn', 'date_publication', 'image', 'description', 'prix', 'disponible']:
                if field in validated_data and validated_data.get(field) not in (None, ''):
                    setattr(existing, field, validated_data.get(field))
            existing.save()
            return existing

        # Sinon créer un nouveau livre normalement
        return super().create(validated_data)
