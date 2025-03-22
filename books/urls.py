from django.urls import path
from .views import (RegisterView, LoginView, CreateBookView, GetBookByID, GetBookReviews, CreateReview,
    SearchBooksByTitle, SearchBooksByAuthor, SearchBooksByGenre, GetTopRatedBooks, GetBookByISBN,
    GetBookAvailability, SearchBooksByPublicationDate, SearchAwardWinningBooks, GetBookMetadata,
    GetAuthorBio, GetAuthorWorks, GetBookRecommendations, SearchBooksByLanguage, SearchBooksByPublisher,
    GetBookPriceComparison, SearchBooksByAgeGroup, GetBookSummary)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Book-related views
    path('book/', CreateBookView.as_view(), name='create_book'),
    path('book/<int:book_id>/', GetBookByID.as_view(), name='get_book_by_id'),
    path('book/<int:book_id>/reviews/', GetBookReviews.as_view(), name='get_book_reviews'),
    path('book/<int:book_id>/reviews/create/', CreateReview.as_view(), name='create_review'),

    # Search endpoints
    path('search/title/<str:title>/', SearchBooksByTitle.as_view(), name='search_books_by_title'),
    path('search/author/<str:author_name>/', SearchBooksByAuthor.as_view(), name='search_books_by_author'),
    path('search/genre/<str:genre>/', SearchBooksByGenre.as_view(), name='search_books_by_genre'),
    path('search/bestsellers/', GetTopRatedBooks.as_view(), name='get_top_rated_books'),
    path('book/isbn/<str:isbn_number>/', GetBookByISBN.as_view(), name='get-book-by-isbn'),
    path('book/<int:book_id>/availability', GetBookAvailability.as_view(), name='book-availability'),
    path('search/pub_date/<str:date>', SearchBooksByPublicationDate.as_view(), name='search-by-date'),
    path('search/awards/<str:award_name>', SearchAwardWinningBooks.as_view(), name='search-by-awards'),
    path('book/<int:book_id>/metadata', GetBookMetadata.as_view(), name='book-metadata'),
    path('author/<str:author_name>/bio', GetAuthorBio.as_view(), name='author-bio'),
    path('author/<str:author_name>/works', GetAuthorWorks.as_view(), name='author-works'),
    path('book/<int:book_id>/recommendations', GetBookRecommendations.as_view(), name='book-recommendations'),
    path('search/language/<str:language>', SearchBooksByLanguage.as_view(), name='search-books-language'),
    path('search/publisher/<str:publisher_name>', SearchBooksByPublisher.as_view(), name='search-books-publisher'),
    path('search/top_rated', GetTopRatedBooks.as_view(), name='top-rated-books'),
    path('search/age_group/<str:age_group>', SearchBooksByAgeGroup.as_view(), name='search-books-age-group'),

    path('book/<int:book_id>/price_comparison', GetBookPriceComparison.as_view(), name='book-price-comparison'),
    path('book/<int:book_id>/summary', GetBookSummary.as_view(), name='book-summary'),


    # Authentication-related views
    path('register/', RegisterView.as_view(), name='register'),  # Custom registration endpoint
    path('login/', LoginView.as_view(), name='login'),  # Custom login endpoint for JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh access token
]