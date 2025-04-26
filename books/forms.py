# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['user']  # Exclude the 'user' field because we will handle it in the view
        fields = '__all__'  # Include all fields except the 'user'
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5}),
        }

    def __init__(self, *args, **kwargs):
        # Accept the user from the view when initializing the form
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_rating(self):
        # Ensure rating is provided if the book is completed
        rating = self.cleaned_data.get('rating')
        if self.instance.status == 'Completed' and rating is None:
            raise forms.ValidationError('Rating is required when the status is "Completed".')
        return rating

    def save(self, commit=True):
        # Automatically associate the book with the current user
        book = super().save(commit=False)
        if self.user:
            book.user = self.user  # Associate with the passed user
        if commit:
            book.save()
        return book

# ✅ Make sure this class exists and is properly indented
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
