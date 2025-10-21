from django.shortcuts import render
from .models import Book

def books_view(request):
    """Страница всех книг"""
    books = Book.objects.all().order_by('pub_date', 'name')
    return render(request, 'books/books_list.html', {'books': books})  

def books_by_date_view(request, pub_date):
    """Страница книг за конкретную дату"""
    books = Book.objects.filter(pub_date=pub_date).order_by('name')
    
    
    prev_book = Book.objects.filter(
        pub_date__lt=pub_date
    ).order_by('-pub_date').first()
    
    next_book = Book.objects.filter(
        pub_date__gt=pub_date
    ).order_by('pub_date').first()

    context = {
        'books': books,
        'current_date': pub_date,
        'prev_date': prev_book.pub_date if prev_book else None,
        'next_date': next_book.pub_date if next_book else None,
    }
    
    return render(request, 'books/books_list.html', context)  