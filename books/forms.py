from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

KEY_WORDS = (
    ("intitle:", "title"),
    ("inauthor:", "author"),
    ("subject:", "subject"),
    ("isbn:", "isbn"),
)


class BookImportForm(forms.Form):

    searched_phrase = forms.CharField(label="What are you looking for?")
    key_word = forms.ChoiceField(choices=KEY_WORDS, label='Choose: title, author, subject or isbn')


class BookSearchForm(forms.Form):

    title = forms.CharField(required=False, label="Title")
    author = forms.CharField(required=False, label="Author")
    date_published_start = forms.DateField(
        required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        label="Date published: from"
    )
    date_published_end = forms.DateField(
        required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        label="Date published: to"
    )
