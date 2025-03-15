from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    summary = models.TextField(null=True, blank=True)
    page_count = models.IntegerField()
    language = models.CharField(max_length=50)
    publisher = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    review_text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'Review for {self.book.title} by {self.reviewer_name}'
