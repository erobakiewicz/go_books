import requests

GOOGLE_API_BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q='


class GoogleBooksAPIConnector:

    def __init__(self, data):
        self.searched_phrase = data.get('searched_phrase')
        self.key_word = data.get('key_word')

    def get_books_list(self):
        response = requests.get(
            url=f'{GOOGLE_API_BASE_URL}{self.key_word}{self.searched_phrase}')
        return response.json().get("items")
