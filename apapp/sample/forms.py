from django import forms

from sample.models import Author, Book


class AuthorForm(forms.ModelForm):
    class Meta:
        fields = ['name']
        model = Author


class BookForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'description', 'pages', 'author']
        model = Book
