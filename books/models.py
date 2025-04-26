from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='books')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=100,
        choices=[('Reading', 'Reading'), ('Completed', 'Completed'), ('Dropped', 'Dropped')]
    )

    review = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        blank=False,  
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Rating must be between 0 and 5"
    )
    
    

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
    
        if self.status != 'Completed':
            self.rating = 0  
            self.end_date = None
        super().save(*args, **kwargs)

class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
            ("can_view_book", "Can view book"),
        ]