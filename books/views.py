from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Book
from .forms import BookForm

def book_list(request):
    """Display all books with search functionality"""
    query = request.GET.get('q')
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'books/book_list.html', context)

def book_detail(request, pk):
    """Display single book details"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

def book_create(request):
    """Create new book"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Create'})

def book_update(request, pk):
    """Update existing book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Update', 'book': book})

def book_delete(request, pk):
    """Delete book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'books/book_confirm_delete.html', {'book': book})