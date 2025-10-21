from django.contrib import admin
from django.urls import path
from books.views import books_view, books_by_date_view

urlpatterns = [
    path('books/<str:pub_date>/', books_by_date_view, name='books_by_date'),
    path('books/', books_view, name='books'),  
    path('', books_view, name='home'),  
    path('admin/', admin.site.urls),
]