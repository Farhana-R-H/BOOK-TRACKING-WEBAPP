from django.urls import path
from .views import homepage_view ,about_view, add_book,edit_book,delete_book,book_log,search_edit_books,reset_password
from.views import book_list,mark_as_completed,unfinished_books_view ,notepad_view,loginview,sign_up,logout_view,new_password,landing_view,contact_view


urlpatterns = [
    path('', landing_view, name='landing'),
    path('home/', homepage_view, name='homeface'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact_us'),
    path('add/', add_book, name='add_book'),
    path('edit/<int:pk>/', edit_book, name='edit_book'),
    path('delete/<int:pk>/', delete_book, name='delete_book'),
    path('log/', book_log, name='book_log'),
    path('editbook/', search_edit_books, name='search_edit_books'),
    path('books/', book_list, name='book_list'),
     path('books/mark_completed/<int:book_id>/', mark_as_completed, name='mark_as_completed'), 
     path('unfinished/', unfinished_books_view, name='unfinished_books'),
    path('notepad', notepad_view, name='notepad'),
    path("login/",loginview,name='login'),
    path("logout/",logout_view,name="logout"),
    path('signup/',sign_up,name='signup'),
    path("reset/",reset_password,name="reset"),
    path("passwordreset/",new_password),
    path('books/<int:pk>/edit/', edit_book, name='edit_book')

]







   

