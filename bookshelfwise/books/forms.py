from django import forms

from books.models import Book, Author, ISBN


# class AuthorForm(ModelForm):
#     class Meta:
#         model = Author
#         fields = '__all__'
#
#
# class ISBNForm(ModelForm):
#     class Meta:
#         model = ISBN
#         fields = '__all__'


class DateTypeInput(forms.DateInput):
    input_type = "date"


class BookAddEditForm(forms.ModelForm):
    # author = AuthorForm
    author = forms.CharField(max_length=128)
    isbn = forms.CharField(max_length=128)
    # publication_date = forms.DateField()

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'publication_date': DateTypeInput
        }
