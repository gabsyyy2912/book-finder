from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, Author, Review
from .serializers import ReviewSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import (BookSerializer, BookAvailabilitySerializer, AuthorBioSerializer,
    AuthorWorksSerializer, AuthorWorksSerializer, BookMetadataSerializer, BookSummarySerializer,
    BookPriceSerializer)


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


class CreateBookView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()

            # ✅ Ensure the full book details (including age_group) are returned
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

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

class GetBookByISBN(APIView):
    def get(self, request, isbn_number):
        book = get_object_or_404(Book, isbn=isbn_number)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetBookAvailability(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookAvailabilitySerializer(book)
        return Response(serializer.data)

class SearchBooksByPublicationDate(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        return Book.objects.filter(publication_date=date)

# ✅ Search for Award-Winning Books
class SearchAwardWinningBooks(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        award_name = self.kwargs['award_name']
        return Book.objects.filter(awards__icontains=award_name)

# ✅ 5. Get Book Metadata
class GetBookMetadata(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookMetadataSerializer(book)
        return Response(serializer.data)

# ✅ 6. Get Author's Biography
class GetAuthorBio(APIView):
    def get(self, request, author_name):
        author = get_object_or_404(Author, name=author_name)

        # Ensure 'bio' exists in the response
        bio = author.bio if author.bio else "Biography not available."

        return Response({"name": author.name, "bio": bio})

# ✅ 7. Get Author's List of Works
class GetAuthorWorks(APIView):
    def get(self, request, author_name):
        author = get_object_or_404(Author, name=author_name)
        serializer = AuthorWorksSerializer(author)
        return Response(serializer.data)

# ✅ 8. Get Book Recommendations
class GetBookRecommendations(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        recommendations = Book.objects.filter(genre=book.genre).exclude(id=book.id)[:5]
        serializer = BookMetadataSerializer(recommendations, many=True)
        return Response(serializer.data)

# ✅ 9. Search Books by Language
class SearchBooksByLanguage(generics.ListAPIView):
    serializer_class = BookMetadataSerializer

    def get_queryset(self):
        language = self.kwargs['language']
        return Book.objects.filter(language__icontains=language)

class SearchBooksByPublisher(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        publisher_name = self.kwargs['publisher_name']
        return Book.objects.filter(publisher__icontains=publisher_name)

class GetTopRatedBooks(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all().order_by('-rating')[:10]

class GetBookPriceComparison(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookPriceSerializer(book)
        return Response(serializer.data)

class SearchBooksByAgeGroup(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        age_group = self.kwargs['age_group']
        return Book.objects.filter(genre__icontains=age_group)

class GetBookSummary(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSummarySerializer(book)
        return Response(serializer.data)


def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()

        # ✅ Print full book object to confirm it's saved correctly
        print("Saved Book Object:", book)

        # ✅ Print serialized book data before returning response
        serialized_data = BookSerializer(book).data
        print("Serialized Response:", serialized_data)

        return Response(serialized_data, status=status.HTTP_201_CREATED)

    print("Serializer Errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
