from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import BookForm, CustomUserCreationForm
from .models import Book
from django.utils import timezone
from django.contrib import messages

# Landing View
def landing_view(request):
    return render(request, "landing.html")

# Homepage View
@login_required
def homepage_view(request):
    return render(request, 'homepage.html')

# About Us View
def about_view(request):
    return render(request, 'aboutus.html')

# Contact Us View
def contact_view(request):
    return render(request, 'contact.html')

# Login View
def loginview(request):
    if request.user.is_authenticated:
        return redirect('homeface')

    if request.method == "POST":
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', 'homeface')
            return redirect(next_url)
        else:
            return render(request, "registration/login.html", {"msg": "Invalid login"})
    else:
        return render(request, "registration/login.html", {'next': request.GET.get('next', '')})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('landing')


# Ensure that logged-in users are redirected to the homepage instead of seeing the sign-up page
def sign_up(request):
    if request.user.is_authenticated:
        # Redirect to homepage if already logged in
        return redirect('homeface')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('homeface')  # Redirect to homepage after successful registration
        else:
            return render(request, 'signup.html', {
                'form': form,
                'msg': 'Invalid signup details',
                'errors': form.errors
            })
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})


# Add Book View
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, "Book added successfully!")
            return redirect('homeface')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

# Edit Book View
@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'edit_book.html', {'form': form, 'book': book})

# Delete Book View
@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('book_list')

# Book List View
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

# Mark Book as Completed
@login_required
def mark_as_completed(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    book.status = "Completed"
    book.end_date = timezone.now().date()
    book.save()
    messages.success(request, "Book marked as completed!")
    return redirect('book_list')

# Unfinished Books View
@login_required
def unfinished_books_view(request):
    search_query = request.GET.get('search', '')
    books = Book.objects.filter(user=request.user, status='unfinished')

    if search_query:
        books = books.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
    
    return render(request, 'unfinished_books.html', {'books': books})

# Search and Edit Books
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

# Book Log View
@login_required
def book_log(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'book_log.html', {'books': books})

# Notepad View
@login_required
def notepad_view(request):
    return render(request, 'books/notepad.html')

# Reset Password View
def reset_password(request):
    if request.method == 'POST':
        # Handle password reset logic here (maybe form submission)
        pass
    return render(request, "reset.html")

# New Password Reset Logic
def new_password(request):
    uname = request.POST.get("username")
    newpwd = request.POST.get('password')

    try:
        user = User.objects.get(username=uname)
        if user:
            user.set_password(newpwd)
            user.save()
            messages.success(request, "New password successfully reset!")
            return render(request, "reset.html", {"msg2": "Password reset successful!"})
    except User.DoesNotExist:
        messages.error(request, "User not found. Password reset failed.")
        return render(request, "reset.html", {"msg2": "Resetting failed!"})
