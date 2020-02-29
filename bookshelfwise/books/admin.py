from django.contrib import admin

from books.models import Book, Author, ISBN

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(ISBN)
