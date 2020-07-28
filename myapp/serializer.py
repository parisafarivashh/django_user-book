from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Book
        fields = ['name', 'price', 'author']


        def create(self, validated_data):
            book = Book.objects.create(
                name = validated_data['name'],
                price = validated_data['price']
            )
            return book
        def update(self, validate_data, instance):
            instance.name = validate_data.get('name', instance.name)
            instance.price = validate_data.get('price', instance.price)
            instance.author = validate_data.get('author', instance.author)
            instance.save()
            return instance