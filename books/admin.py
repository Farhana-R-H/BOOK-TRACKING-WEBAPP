from django.contrib import admin
from .models import (
    Book, ReadingSession, Note, Profile, WishlistBook,
    Review, ReadingGoal, Prompt, UserPromptAnswer
)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'status', 'start_date', 'end_date', 'rating')
    list_filter = ('status', 'genre')
    search_fields = ('title', 'author', 'genre')
    ordering = ('title',)
    fields = ('title', 'author', 'genre', 'cover', 'start_date', 'end_date', 'status', 'review', 'rating')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(user=request.user)

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_snippet', 'active', 'start_date', 'end_date')
    list_filter = ('active', 'start_date', 'end_date')
    search_fields = ('question',)

    def question_snippet(self, obj):
        return obj.question[:75] + ('...' if len(obj.question) > 75 else '')
    question_snippet.short_description = 'Question'

@admin.register(UserPromptAnswer)
class UserPromptAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt_snippet', 'answered_at')
    list_filter = ('answered_at',)
    search_fields = ('user__username', 'answer')

    def prompt_snippet(self, obj):
        return obj.prompt.question[:50] + ('...' if len(obj.prompt.question) > 50 else '')
    prompt_snippet.short_description = 'Prompt'

@admin.register(ReadingSession)
class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = ('book', 'date', 'pages_read')
    list_filter = ('date',)
    search_fields = ('book__title',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'content')
    search_fields = ('user__username', 'content')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'date_of_birth', 'gender', 'joined_date')
    search_fields = ('user__username', 'full_name', 'email')

@admin.register(WishlistBook)
class WishlistBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'read', 'added_at')
    list_filter = ('read',)
    search_fields = ('user__username', 'name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    search_fields = ('user__username', 'text')

@admin.register(ReadingGoal)
class ReadingGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'goal', 'books_read_this_year')
    search_fields = ('user__username',)
