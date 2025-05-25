from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
from django.db.models import Sum
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_pages = models.PositiveIntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=100,
        choices=[('Reading', 'Reading'), ('Completed', 'Completed'), ('Dropped', 'Dropped')]
    )

    review = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        null=False,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Rating must be between 0 and 5"
    )

    def __str__(self):
        return self.title

    @property
    def pages_read(self):
        total = self.sessions.aggregate(total_pages=Sum('pages_read'))['total_pages']
        return total or 0

    @property
    def pages_left(self):
        if self.total_pages:
            return max(self.total_pages - self.pages_read, 0)
        return None

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save first to generate primary key

        # Now safely access related sessions
        if self.total_pages and self.pages_read >= self.total_pages:
            if self.status != 'Completed':
                self.status = 'Completed'
                if not self.end_date:
                    self.end_date = timezone.now().date()
                super().save(update_fields=['status', 'end_date'])  # update only changed fields



class ReadingSession(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    pages_read = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.date}: {self.pages_read} pages"

    class Meta:
        ordering = ['-date']

        
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Note {self.id} by {self.user.username}"
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class WishlistBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class ReadingGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reading_goal')
    year = models.PositiveIntegerField(default=now().year)
    goal = models.PositiveIntegerField(default=30)

    def books_read_this_year(self):
        return self.user.books.filter(status='Completed', end_date__year=self.year).count()

    def __str__(self):
        return f"{self.user.username} - {self.year} Goal: {self.goal} books"


class Prompt(models.Model):
    question = models.TextField()
    active = models.BooleanField(default=False)  # Optional if using dates
    start_date = models.DateField(null=True, blank=True)  # When prompt becomes active
    end_date = models.DateField(null=True, blank=True)    # When prompt expires

    def __str__(self):
        return self.question[:50]  # Show first 50 chars in admin

    class Meta:
        ordering = ['-start_date']  # Most recent first


class UserPromptAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    answer = models.TextField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prompt.id} answered on {self.answered_at.strftime('%Y-%m-%d')}"