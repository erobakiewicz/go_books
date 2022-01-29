from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, FormView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from books.api.google_api import GoogleBooksAPIConnector
from books.api.serializers import BookSerializer
from books.forms import BookImportForm
from books.models import Book


class BookListView(ListView):
    queryset = Book.objects.all()


class BookCreateView(CreateView):
    model = Book
    fields = ["title", "author", "date_published", "ISBN", "pages", "cover_url", "language"]

    def get_success_url(self):
        return reverse("books:book_list")


class AddBookAPIView(CreateAPIView):
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListBooksViewSet(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["title", "author", "date_published", "ISBN", "pages", "cover_url", "language"]
    search_fields = ["title", "author", "date_published", "ISBN", "pages", "cover_url", "language"]


class ImportBooks(FormView):
    template_name = 'importer.html'
    form_class = BookImportForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.imported_books = []

    def get_success_url(self):
        return reverse("books:import")

    def get_context_data(self, **kwargs):
        return {
            'imported_books': self.imported_books,
            **super().get_context_data(**kwargs)
        }

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = self.get_form_kwargs().get("data")
            google_api = GoogleBooksAPIConnector(data)
            results = self.get_formatted_results(google_api.get_books_list())
            for obj in results:
                serializer = BookSerializer(data=obj)
                serializer.is_valid(raise_exception=True)
                imported_book, created = Book.objects.get_or_create(**serializer.validated_data)
                if created:
                    self.imported_books.append(imported_book)
            return render(request, "importer.html", self.get_context_data())
        else:
            return self.form_invalid(form)

    def get_formatted_results(self, results):
        if results:
            return [self.get_book_dict(item) for item in results]
        return None

    def get_book_dict(self, item):
        book_info = item.get('volumeInfo')
        return {
            "id": item.get("id"),
            "title": book_info.get("title", ''),
            "author": self.get_from_list(book_info.get("authors", '')),
            "date_published": book_info.get("publishedDate", None),
            "ISBN": self.get_isbn(book_info.get("industryIdentifiers", '')),
            "pages": int(book_info.get("pageCount", 0)),
            "cover_url": self.get_img_link(book_info.get("imageLinks", None)),
            "language": book_info.get("language", ''),
        }

    @staticmethod
    def get_from_list(info_list):
        return ', '.join([item for item in info_list])

    @staticmethod
    def get_isbn(identifiers_list):
        if identifiers_list:
            if isbn_list := [item for item in identifiers_list if item.get("type") == "ISBN_13"]:
                return isbn_list[0].get("identifier")
        return ''

    @staticmethod
    def get_img_link(img_links):
        if img_links:
            if thumbnail := img_links.get("thumbnail"):
                return thumbnail
            elif small_thumbnail := img_links.get("smallThumbnail"):
                return small_thumbnail
            else:
                return None
        return None
