# books/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, Author, Review
from .serializers import BookSerializer, AuthorSerializer, ReviewSerializer
from django.db.models import Q

class SearchBooksByTitle(APIView):
    def get(self, request, title):
        books = Book.objects.filter(title__icontains=title)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class SearchBooksByAuthor(APIView):
    def get(self, request, author_name):
        books = Book.objects.filter(author__name__icontains=author_name)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class SearchBooksByGenre(APIView):
    def get(self, request, genre):
        books = Book.objects.filter(genre__icontains=genre)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class GetBookByISBN(APIView):
    def get(self, request, isbn_number):
        try:
            book = Book.objects.get(isbn=isbn_number)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class GetBookByID(APIView):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class GetBookReviews(APIView):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            reviews = book.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class GetBookAvailability(APIView):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            availability = {"available": True}  # You can replace with actual availability check
            return Response(availability)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class SearchBooksByPublicationDate(APIView):
    def get(self, request, date):
        books = Book.objects.filter(publication_date=date)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class GetTopRatedBooks(APIView):
    def get(self, request):
        books = Book.objects.all().order_by('-id')  # You can customize this to order by rating or other criteria
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class GetBookSummary(APIView):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            return Response({"summary": book.summary})
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateBook(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
