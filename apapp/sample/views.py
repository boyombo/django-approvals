from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from sample.models import Author, Book
from sample.forms import AuthorForm, BookForm
from sample.approval_template import BookApproval


class AuthorListView(ListView):
    model = Author
    template_name = 'authors.html'


def edit_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            obj = form.save(commit=False)
            BookApproval(request.user, obj)
            return redirect('authors')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'edit_author.html', {'form': form})


class BookListView(ListView):
    model = Book
    template_name = 'books.html'


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            obj = form.save(commit=False)
            BookApproval(request.user, obj)
            return redirect('books')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})
