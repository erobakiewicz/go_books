from django import forms

KEY_WORDS = (
    ("intitle:", "title"),
    ("inauthor:", "author"),
    ("subject:", "subject"),
    ("isbn:", "isbn"),
)


class BookImportForm(forms.Form):
    searched_phrase = forms.CharField(help_text="What are you looking for?")
    key_word = forms.ChoiceField(choices=KEY_WORDS)


class BookSearchForm(forms.Form):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    date_published_start = forms.DateField(
        required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
    )
    date_published_end = forms.DateField(
        required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
    )
