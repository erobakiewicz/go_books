from django.urls import reverse
from django.views.generic import ListView, CreateView
from rest_framework.viewsets import ModelViewSet

from books.api.serializers import BookSerializer
from books.models import Book


class BookListView(ListView):
    queryset = Book.objects.all()


class BookCreateView(CreateView):
    model = Book
    fields = ["title", "author", "date_published", "ISBN", "pages", "cover_url", "language"]

    def get_success_url(self):
        return reverse("books:book_list")


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
