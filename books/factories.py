import datetime

import factory.django
from factory import fuzzy

from books.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda i: "title {}".format(i))
    author = factory.Sequence(lambda i: "author {}".format(i))
    date_published = fuzzy.FuzzyDate(
        datetime.date(1018, 1, 1),
        datetime.date(2022, 12, 31),
    )
    language = factory.Sequence(lambda i: "language {}".format(i))

    class Meta:
        model = Book
