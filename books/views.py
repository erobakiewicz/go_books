from django.shortcuts import render
from django.views.generic import ListView

from books.models import Book


class BookListView(ListView):
    queryset = Book.objects.all()