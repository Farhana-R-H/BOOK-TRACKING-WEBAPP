from django.urls import path
from .views import homepage_view ,about_view, add_book,edit_book,delete_book,book_log,search_edit_books,profile_view, view_note,edit_profile_view,mark_as_read,delete_books,password_reset_request_view,dashboard_view,reading_books_view
from.views import book_list,mark_as_completed,unfinished_books_view ,notepad_view,contact_view,review_view,signup,login_view,home,logout_view,delete_note,wishlist_view, submit_review,edit_note,set_new_password_view, add_reading_session


urlpatterns = [
     path('', home, name='home'),
    path('homeface/', homepage_view, name='homeface'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/',profile_view, name='profile'),
    path('reset-password/', password_reset_request_view, name='password_reset_request'),
    path('set-new-password/', set_new_password_view, name='set_new_password'),
    # path('wishlist/toggle/<int:item_id>/', toggle_wishlist_item, name='toggle_wishlist_item'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
      path('delete_books/<int:book_id>/', delete_books, name='delete_books'),
    path('wishlist/', wishlist_view, name='wishlist'),
     path('review/', review_view, name='review'), 
    
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact_us'),
    path('add/', add_book, name='add_book'),
     path('submit-review/', submit_review, name='submit_review'),
    path('edit/<int:pk>/', edit_book, name='edit_book'),
    path('delete/<int:pk>/', delete_book, name='delete_book'),
    path('log/', book_log, name='book_log'),
    path('editbook/', search_edit_books, name='search_edit_books'),
    path('books/', book_list, name='book_list'),
    path('books/mark_completed/<int:book_id>/', mark_as_completed, name='mark_as_completed'),
      


    path('unfinished/', unfinished_books_view, name='unfinished_books'),
    path('notepad', notepad_view, name='notepad'),
    path('notepad/delete/<int:note_id>/', delete_note, name='delete_note'),
    path('notepad/<int:note_id>/', view_note, name='view_note'),
    path('edit-note/<int:note_id>/', edit_note, name='edit_note'),
    
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('mark-read/<int:book_id>/', mark_as_read, name='mark_as_read'),
    path('dashboard/', dashboard_view, name='dashboard'),
     path('books/reading/', reading_books_view, name='reading_books'),
     path('reading/<int:book_id>/add-session/', add_reading_session, name='add_reading_session'),


]







   

