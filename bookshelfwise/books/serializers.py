from rest_framework import serializers

from books.models import Book, Author, ISBN


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ISBNSerializer(serializers.ModelSerializer):
    class Meta:
        model = ISBN
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    isbn = ISBNSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'
