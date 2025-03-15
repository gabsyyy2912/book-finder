# book_finder/urls.py (or your project folder's main `urls.py`)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),  # Make sure this line is included
    path("", include("books.urls")),
]
