from django.urls import path

from books.views import BookListView

app_name = 'books'

urlpatterns = [
    path("", BookListView.as_view(), name="book_list")
]
