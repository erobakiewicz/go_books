from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.factories import BookFactory
from books.google_api_response_test_data import GOOGLE_API_TEST_DATA
from books.models import Book


class BooksViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.book1 = BookFactory()
        cls.book2 = BookFactory(language="PL")
        cls.book3 = BookFactory(language="PL")

    def test_list_books_view(self):
        response = self.client.get(reverse("books:book_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.book1.title, response.content.decode('utf-8'))
        self.assertIn(self.book2.title, response.content.decode('utf-8'))
        self.assertIn(self.book3.title, response.content.decode('utf-8'))

    def test_list_books_search_engine_find_book1_by_title(self):
        response = self.client.get(reverse("books:book_list"), data={"title": self.book1.title})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context_data.get("object_list")), 1)
        self.assertEqual(response.context_data.get("object_list").first(), self.book1)

    def test_list_books_search_engine_find_all_books_with_the_same_langauge_param(self):
        response = self.client.get(reverse("books:book_list"), data={"language": "PL"})
        self.assertEqual(len(response.context_data.get("object_list").filter(language="PL")), 2)

    def test_create_book_view(self):
        response = self.client.post(reverse("books:book_create"), data={
            "title": "Test title",
            "author": "Test author",
            "date_published": "2020-01-01",
            "ISBN": "979-1937-91-197-2",
            "pages": 222,
            "cover_url": "https://test.test",
            "language": "PL"
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("books:book_list"))
        self.assertTrue(Book.objects.get(title="Test title"))


class BooksAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.book1 = BookFactory()
        cls.book2 = BookFactory()
        cls.book3 = BookFactory()

    def test_add_book_api_view(self):
        response = self.client.post(
            reverse('books_api:add_book'),
            data={
                "title": "Test title",
                "author": "Test author",
                "date_published": "2020-01-01",
                "ISBN": "979-1937-91-197-2",
                "pages": 222,
                "cover_url": "https://test.test",
                "language": "PL"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_books_api_view(self):
        response = self.client.get(reverse('books_api:list_books'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_books_api_view_returns_list_of_books_in_db(self):
        response = self.client.get(reverse('books_api:list_books'))
        self.assertEqual(len(response.json()), Book.objects.all().count())
        for obj in response.json():
            self.assertTrue(obj.get("title") in [self.book1.title, self.book2.title, self.book3.title])


class GoogleBooksAPITestCase(TestCase):

    @patch('books.api.google_api.GoogleBooksAPIConnector.get_books_list')
    def test_empty_response_do_not_create_objects(self, mock_google_api):
        mock_google_api.return_value = {
            "kind": "books#volumes",
            "totalItems": 0
        }

        response = self.client.post(reverse('books:import'), data={
            "searched_phrase": "123qweasd!@#",
            "key_word": "intitle:"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.all().count(), 0)

    @patch('books.api.google_api.GoogleBooksAPIConnector.get_books_list')
    def test_create_three_books_from_api_response(self, mock_google_api):
        mock_google_api.return_value = GOOGLE_API_TEST_DATA
        response = self.client.post(reverse('books:import'), data={
            "searched_phrase": "Tolkien",
            "key_word": "intitle:"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.all().count(), 3)
