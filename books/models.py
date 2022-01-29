from django.db import models


class Book(models.Model):
    title = models.CharField("Title", max_length=250)
    author = models.CharField("Author", max_length=250)
    date_published = models.CharField("Date published", max_length=100)
    ISBN = models.CharField("ISBN number", max_length=25, null=True, blank=True)
    pages = models.PositiveSmallIntegerField("Pages")
    cover_url = models.URLField("Cover url", null=True, blank=True)
    language = models.CharField("Language", max_length=100)

    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
