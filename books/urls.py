from django.urls import path
from .views import RegisterView, LoginView, CreateBook, GetBookByID, GetBookReviews, CreateReview, SearchBooksByTitle, \
    SearchBooksByAuthor, SearchBooksByGenre, GetTopRatedBooks
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Book-related views
    path('book/', CreateBook.as_view(), name='create_book'),
    path('book/<int:book_id>/', GetBookByID.as_view(), name='get_book_by_id'),
    path('book/<int:book_id>/reviews/', GetBookReviews.as_view(), name='get_book_reviews'),
    path('book/<int:book_id>/reviews/create/', CreateReview.as_view(), name='create_review'),

    # Search endpoints
    path('search/title/<str:title>/', SearchBooksByTitle.as_view(), name='search_books_by_title'),
    path('search/author/<str:author_name>/', SearchBooksByAuthor.as_view(), name='search_books_by_author'),
    path('search/genre/<str:genre>/', SearchBooksByGenre.as_view(), name='search_books_by_genre'),
    path('search/bestsellers/', GetTopRatedBooks.as_view(), name='get_top_rated_books'),

    # Authentication-related views
    path('register/', RegisterView.as_view(), name='register'),  # Custom registration endpoint
    path('login/', LoginView.as_view(), name='login'),  # Custom login endpoint for JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh access token
]
