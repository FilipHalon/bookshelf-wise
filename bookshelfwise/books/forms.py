from django import forms

from books.models import Book


class BookAddEditForm(forms.ModelForm):
    # author = forms.CharField(max_length=128)
    # isbn = forms.CharField(max_length=128)
    # publication_date = forms.DateField()

    class Meta:
        model = Book
        fields = '__all__'
