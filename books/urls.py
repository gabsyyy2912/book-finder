# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/title/<str:title>/', views.SearchBooksByTitle.as_view(), name='search_books_by_title'),
    path('search/author/<str:author_name>/', views.SearchBooksByAuthor.as_view(), name='search_books_by_author'),
    path('search/genre/<str:genre>/', views.SearchBooksByGenre.as_view(), name='search_books_by_genre'),
    path('book/isbn/<str:isbn_number>/', views.GetBookByISBN.as_view(), name='get_book_by_isbn'),
    path('book/<int:book_id>/', views.GetBookByID.as_view(), name='get_book_by_id'),
    path('book/<int:book_id>/reviews/', views.GetBookReviews.as_view(), name='get_book_reviews'),
    path('book/<int:book_id>/availability/', views.GetBookAvailability.as_view(), name='get_book_availability'),
    path('search/pub_date/<str:date>/', views.SearchBooksByPublicationDate.as_view(), name='search_books_by_pub_date'),
    path('search/bestsellers/', views.GetTopRatedBooks.as_view(), name='get_top_rated_books'),
    path('book/<int:book_id>/summary/', views.GetBookSummary.as_view(), name='get_book_summary'),
    path('book/', views.CreateBook.as_view(), name='create_book'),
]
