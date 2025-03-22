from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    AGE_GROUP_CHOICES = [
        ('kids', 'Kids'),
        ('teens', 'Teens'),
        ('adults', 'Adults'),
    ]
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    summary = models.TextField(blank=True, null=True)
    page_count = models.IntegerField()
    language = models.CharField(max_length=50)
    publisher = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    awards = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # For price comparison
    retailer = models.CharField(max_length=255, blank=True, null=True)  # Store retailer names for price comparison
    rating = models.FloatField(default=0.0)  # Used for top-rated boo
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    review_text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'Review for {self.book.title} by {self.reviewer_name}'