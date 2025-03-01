# books/serializers.py
from rest_framework import serializers
from .models import Book, Author, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be exactly 13 characters.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
