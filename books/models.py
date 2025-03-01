# books/models.py
from django.db import models

# books/models.py
# books/models.py
class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(default="This author has not provided a biography.")

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    publication_date = models.DateField()
    page_count = models.IntegerField()
    language = models.CharField(max_length=50)
    publisher = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review of {self.book.title} by {self.reviewer_name}"
