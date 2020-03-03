from django import forms

from books.models import Book


class DateTypeInput(forms.DateInput):
    input_type = "date"


class BookCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'publication_date': DateTypeInput,
            'author': forms.TextInput,
            'isbn': forms.TextInput
        }


class GoogleBookAPISearchForm(forms.Form):
    q = forms.CharField(max_length=128, label="Search phrase*", help_text="Browse through the API as you would do in any Google search.")
    intitle = forms.CharField(max_length=128, required=False, label="Title")
    inauthor = forms.CharField(max_length=128, required=False, label="Author")
    isbn = forms.CharField(max_length=32, required=False, label="ISBN")
