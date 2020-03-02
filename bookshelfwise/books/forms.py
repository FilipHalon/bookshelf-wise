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
