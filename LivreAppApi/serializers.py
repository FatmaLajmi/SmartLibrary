from rest_framework import serializers
from LivreApp.models import Livre
from django.db import transaction

class LivreSerializer(serializers.ModelSerializer):
    # Optional temporary field for image upload when using BLOB
    image_upload = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Livre
        fields = '__all__'
        read_only_fields = ('date_added', 'date_modified', 'image_blob')

    @transaction.atomic
    def create(self, validated_data):
        # Retrieve uploaded image if present
        image_file = validated_data.pop('image_upload', None)

        title = validated_data.get('title', '').strip()
        author = validated_data.get('author', '').strip()
        quantity_new = validated_data.get('quantity', 1)

        # Check if a book with the same title and author already exists
        existing = Livre.objects.filter(title__iexact=title, author__iexact=author).first()
        if existing:
            existing.quantity += quantity_new
            # Update other fields if provided
            for field in ['isbn', 'publication_date', 'description', 'price', 'available']:
                if field in validated_data and validated_data.get(field) not in (None, ''):
                    setattr(existing, field, validated_data.get(field))
            # Update image BLOB
            if image_file:
                existing.image_blob = image_file.read()
            existing.save()
            return existing

        # Otherwise, create a new book
        if image_file:
            validated_data['image_blob'] = image_file.read()
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        # Update image if uploaded
        image_file = validated_data.pop('image_upload', None)
        if image_file:
            instance.image_blob = image_file.read()
        return super().update(instance, validated_data)
