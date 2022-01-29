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
