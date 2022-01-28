from django.urls import path

from books.views import BookListView, BookCreateView

app_name = 'books'

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path('create/', BookCreateView.as_view(), name="book_create"),
]
