from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book , Note
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from .forms import BookForm , NoteForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import ProfileForm , ReviewForm 
from.models import Profile , Review
from .models import WishlistBook  , ReadingSession
from django.http import JsonResponse
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from.forms import PasswordResetRequestForm , ReadingSessionForm , ReadingGoalForm
from django.db.models import Count, Sum, F, ExpressionWrapper, DurationField 
from django.utils.timezone import now
from datetime import timedelta
from.models import ReadingGoal , UserPromptAnswer , Prompt


def home(request):
    latest_reviews = Review.objects.select_related('user').order_by('-created_at')[:8]  # Fetch latest 10 reviews
    return render(request, 'accounts/home.html', {'latest_reviews': latest_reviews})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']

            base_username = f"{first_name}{last_name}".replace(" ", "").lower()
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user = User(username=username, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()

            # Redirect to login page with username and password as GET params (only for demo purposes!)
            login_url = f"{reverse('login')}?username={username}&password={password}"
            return HttpResponseRedirect(login_url)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})




def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(username=username)
                if user.profile.email == email:
                    # Save user ID to session and redirect to new password page
                    request.session['reset_user_id'] = user.id
                    return redirect('set_new_password')
                else:
                    messages.error(request, "Email does not match our records.")
            except User.DoesNotExist:
                messages.error(request, "User with this username does not exist.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form}) 



def login_view(request):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homeface')
    else:
        # Prefill username and password on GET request
        form = AuthenticationForm(request, initial={'username': username, 'password': password})

    return render(request, 'accounts/login.html', {'form': form})




def dashboard_view(request):
    user = request.user

    # Top 3 most reviewed books (by rating & review presence)
    top_books = Book.objects.filter(user=user, rating__gt=0, review__isnull=False).order_by('-rating')[:3]

    # Count of completed books
    completed_books_count = Book.objects.filter(user=user, status='Completed').count()

    # Calculate the start of the current month
    current_month_start = now().replace(day=1)

    # Pages read this month
    pages_read_this_month = ReadingSession.objects.filter(
        book__user=user,
        date__gte=current_month_start
    ).aggregate(total=Sum('pages_read'))['total'] or 0

    # Fastest book
    fastest_book = Book.objects.filter(
        user=user,
        start_date__isnull=False,
        end_date__isnull=False
    ).annotate(
        duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField())
    ).order_by('duration').first()

    # Longest book
    longest_book = Book.objects.filter(user=user).order_by('-total_pages').first()

    # 📘 Reading Goal Setup
    current_year = now().year
    goal, _ = ReadingGoal.objects.get_or_create(user=user, year=current_year)

    # Handle form submission
    if request.method == 'POST':
        form = ReadingGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
    else:
        form = ReadingGoalForm(instance=goal)

    books_read = goal.books_read_this_year()
    progress = int((books_read / goal.goal) * 100) if goal.goal else 0

    context = {
        'top_books': top_books,
        'completed_books_count': completed_books_count,
        'pages_read_this_month': pages_read_this_month,
        'fastest_book': fastest_book,
        'longest_book': longest_book,
        'form': form,
        'goal': goal,
        'books_read': books_read,
        'progress': progress,
    }

    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to landing/home page




def set_new_password_view(request):
    if 'reset_user_id' not in request.session:
        return redirect('password_reset_request')  # Force them to go through check first

    user = User.objects.get(id=request.session['reset_user_id'])

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
        else:
            user.password = make_password(new_password)
            user.save()
            del request.session['reset_user_id']  # Clean up
            messages.success(request, "Password reset successful.")
            return redirect('login')
    return render(request, 'accounts/set_new_password.html')




@login_required
def homepage_view(request):
    return render(request, 'homepage.html')



def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # assuming Review model has a user ForeignKey
            review.save()
            return redirect('home')  # or wherever you want to go after submission
    else:
        form = ReviewForm()
    return render(request, 'review.html', {'form': form})




@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            saved_profile = form.save()
            messages.success(request, 'Profile updated successfully.')
            print("Saved profile picture:", saved_profile.profile_picture.name)
            return redirect('profile')
        else:
            print("Form errors:", form.errors)  # Debug print to see form errors
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})





@login_required
def profile_view(request):
    user = request.user

    # Handle wishlist book read status update
    if request.method == 'POST' and 'book_id' in request.POST:
        book_id = request.POST.get('book_id')
        try:
            book = WishlistBook.objects.get(id=book_id, user=user)
            book.read = True
            book.save()
            return redirect('profile')
        except WishlistBook.DoesNotExist:
            pass  # Could add error handling here

    # Handle prompt answer submission
    if request.method == 'POST' and 'prompt_answer' in request.POST:
        answer = request.POST.get('prompt_answer', '').strip()
        # Find the active prompt that user hasn't answered yet
        active_prompt = Prompt.objects.filter(
            active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).exclude(
            userpromptanswer__user=user
        ).first()

        if active_prompt and answer:
            UserPromptAnswer.objects.create(user=user, prompt=active_prompt, answer=answer)
            return redirect('profile')  # Prevent resubmission

    # GET request or fallback data
    priority_books = WishlistBook.objects.filter(user=user, read=False).order_by('-added_at')[:10]

    # Get active prompt for user (unanswered)
    active_prompt = Prompt.objects.filter(
        active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).exclude(
        userpromptanswer__user=user
    ).first()

    # Get previous prompt answers for user
    previous_answers = UserPromptAnswer.objects.filter(user=user).order_by('-answered_at')[:10]

    context = {
        'priority_books': priority_books,
        'active_prompt': active_prompt,
        'previous_answers': previous_answers,
    }

    return render(request, 'profile.html', context)
@login_required
def wishlist_view(request):
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        if book_name:
            WishlistBook.objects.create(user=request.user, name=book_name)
            return redirect('wishlist')

    wishlist = WishlistBook.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'wishlist.html', {'wishlist': wishlist})




@login_required
def mark_as_read(request, book_id):
    book = WishlistBook.objects.get(id=book_id, user=request.user)
    book.is_read = True
    book.save()
    return redirect('profile')




@login_required
def delete_books(request, book_id):
    if request.method == 'POST':
        # get the book that belongs to this user
        book = get_object_or_404(WishlistBook, id=book_id, user=request.user)
        book.delete()
    return redirect('wishlist')




def review_view(request):
    return render(request, 'review.html')


def about_view(request):
    return render(request, 'aboutus.html')


def contact_view(request):
    return render(request, 'contact.html')



@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()  # first save to assign PK
            messages.success(request, "Book added successfully!")
            return redirect('homeface')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})





@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('search_edit_books')  # <-- Redirect here
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})





@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('search_edit_books')




@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        status = request.POST.get('status')
        
        new_book = Book(title=title, author=author, status=status, user=request.user)
        new_book.save()
        messages.success(request, "New book added successfully!")
        return redirect('book_list')
    
    return render(request, 'book_list.html', {'books': books})




@login_required
def mark_as_completed(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    book.status = "Completed"
    book.end_date = timezone.now().date()
    book.save()
    messages.success(request, "Book marked as completed!")
    return redirect('book_list')




@login_required
def unfinished_books_view(request):
    search_query = request.GET.get('search', '')
    
    # Filter books by 'unfinished', 'reading', or 'dropped' statuses
    books = Book.objects.filter(user=request.user).filter(
        Q(status='unfinished') | Q(status='dropped')
    )

    # If a search query is provided, filter the books based on title or author
    if search_query:
        books = books.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
    
    return render(request, 'unfinished_books.html', {'books': books})





@login_required
def search_edit_books(request):
    query = request.GET.get('q', '')
    
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(status__icontains=query),
            user=request.user
        )
    else:
        books = Book.objects.filter(user=request.user)
    
    return render(request, 'books/editbook.html', {'books': books, 'query': query})




@login_required
def book_log(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'book_log.html', {'books': books})




@login_required
def notepad_view(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note saved!")
            return redirect('notepad')
    else:
        form = NoteForm()

    return render(request, 'books/notepad.html', {'notes': notes, 'form': form})




@login_required
def edit_note(request, note_id):
    if request.method == 'POST':
        note = Note.objects.get(id=note_id, user=request.user)
        data = json.loads(request.body)
        note.content = data.get('content', note.content)
        note.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    messages.success(request, "Note deleted.")
    return redirect('notepad')
def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    return render(request, 'view_note.html', {'note': note})




def reading_books_view(request):
    user = request.user
    reading_books = Book.objects.filter(user=user, status='Reading')
    return render(request, 'books/reading_books.html', {'books': reading_books})



def add_reading_session(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    
    # Get reading sessions using the correct related name
    sessions = book.sessions.all()

    if request.method == 'POST':
        form = ReadingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.book = book
            session.save()

            # Book status and end_date are auto-handled by save() in Book model
            book.save()

            return redirect('reading_books')  # Adjust this if needed
    else:
        form = ReadingSessionForm(initial={'date': timezone.now().date()})

    context = {
        'form': form,
        'book': book,
        'sessions': sessions,
        'pages_left': book.pages_left,
    }
    return render(request, 'add_reading_session.html', context)