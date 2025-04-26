from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'status', 'start_date', 'end_date', 'rating')
    list_filter = ('status', 'genre')
    search_fields = ('title', 'author', 'genre')
    ordering = ('title',)
    fields = ('title', 'author', 'genre', 'cover', 'start_date', 'end_date', 'status', 'review', 'rating')
   
class Meta:
        model = Book
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'user', 'created_at')
    list_filter = ('status', 'user')  # Admin can filter by user and status
    search_fields = ['title', 'author', 'user__username']  # Admin can search by title, author, and username
    ordering = ('created_at',)

    def get_queryset(self, request):
        
        # If the user is an admin, return all books; if not, return only the books of the logged-in user
        if request.user.is_superuser:
            return super().get_queryset(request) # Admin sees all books
        return super().get_queryset(request).filter(user=request.user)
