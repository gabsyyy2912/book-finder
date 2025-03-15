from rest_framework import serializers
from .models import Book, Author, Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'book', 'reviewer_name', 'review_text', 'rating']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()  # Nested serializer for author details
    reviews = ReviewSerializer(many=True, read_only=True)  # Nested serializer for reviews

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'isbn', 'publication_date', 'summary', 'page_count', 'language',
                  'publisher', 'reviews']

    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        # If author data is passed, we create the author if it doesn't exist
        if author_data:
            author, created = Author.objects.get_or_create(name=author_data['name'], bio=author_data.get('bio', ''))
            validated_data['author'] = author

        # Create and return the book instance
        book = Book.objects.create(**validated_data)
        return book
