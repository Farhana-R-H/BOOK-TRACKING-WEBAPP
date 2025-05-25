from django import forms
from .models import Book ,Note
import random
from django.contrib.auth.models import User
from .models import Profile , Review
from .models import ReadingSession
from .models import ReadingGoal





class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    agree_terms = forms.BooleanField(label='I agree to the Terms and Conditions', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']  # Remove password here!

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
# class LoginForm(forms.Form):
#     username = forms.CharField(label='Username')
#     password = forms.CharField(widget=forms.PasswordInput, label='Password')
# BookForm: This form allows a user to create or update a Book ins
# 
# 
# tance.
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['user']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5}),
            'total_pages': forms.NumberInput(attrs={'min': 1}),
            # Removed pages_read widget since not a model field
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        rating = cleaned_data.get('rating')
        review = cleaned_data.get('review')
        total_pages = cleaned_data.get('total_pages')

        # For completed books, ensure rating and review are given
        if status == 'Completed':
            if rating is None:
                self.add_error('rating', 'Rating is required when the status is "Completed".')
            if not review:
                self.add_error('review', 'Review is required when the status is "Completed".')
            
            # You cannot validate pages_read here because it comes from sessions
            # But if you want, you could check in your view or model if pages_read == total_pages
            # Or raise a warning elsewhere.

        return cleaned_data

    def save(self, commit=True):
        book = super().save(commit=False)
        if self.user:
            book.user = self.user
        if commit:
            book.save()
        return book


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your note...'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'full_name','email', 'date_of_birth', 'bio', 'gender']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'profile_picture': forms.ClearableFileInput(),
        }
class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    email = forms.EmailField(label="Email") 
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'What do you think about the website?',
            }),
            'rating': forms.HiddenInput(),  # Set by JS
        }

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        word_count = len(text.strip().split())

        if word_count > 50:
            raise forms.ValidationError("Your review must not exceed 50 words.")
        return text


class ReadingSessionForm(forms.ModelForm):
    class Meta:
        model = ReadingSession
        fields = ['date', 'pages_read']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }



class ReadingGoalForm(forms.ModelForm):
    class Meta:
        model = ReadingGoal
        fields = ['goal']
        labels = {'goal': 'Yearly Book Goal'}