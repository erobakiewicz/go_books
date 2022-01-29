from django.urls import path

from books.views import AddBookAPIView, ListBooksViewSet

app_name = "books_api"

urlpatterns = [
    path(r'add_book/', AddBookAPIView.as_view(), name="add_book"),
    path(r'list_books/', ListBooksViewSet.as_view(), name="list_books"),
]
