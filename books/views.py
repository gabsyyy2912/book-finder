from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, Author, Review
from .serializers import BookSerializer, AuthorSerializer, ReviewSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "No active account found with the given credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({"detail": "Account is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        # Create JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    pass


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"detail": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user without tokens
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True  # Ensure the user is active
        user.save()

        # Return only the username and password in the response
        return Response({
            "username": user.username,
            "password": password,  # You should be cautious about exposing the password. Only send it if necessary.
        }, status=status.HTTP_201_CREATED)


class CreateBook(APIView):
    def post(self, request):
        # Pass the data directly to the serializer
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            # Save the book (author will be handled by the serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBookByID(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class GetBookReviews(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        reviews = book.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class CreateReview(APIView):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        request.data['book'] = book.id  # Automatically associate review with the book
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class GetTopRatedBooks(APIView):
    def get(self, request):
        books = Book.objects.all().order_by('-id')  # You can customize this to order by rating or other criteria
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
