from rest_framework import serializers

from books.models import Book, Author, ISBN


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class ISBNSerializer(serializers.ModelSerializer):
    class Meta:
        model = ISBN
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    isbn = ISBNSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        author_list = Book.get_m2m_id_list("serializer", validated_data, "author")
        isbn_list = Book.get_m2m_id_list("serializer", validated_data, "isbn")
        try:
            book = Book.objects.get(
                title=validated_data.get("title"), isbn=isbn_list[0]
            )
            book = Book(pk=book.pk, **validated_data)
        except Book.DoesNotExist:
            book = Book.objects.create(**validated_data)
        book.author.set(author_list)
        book.isbn.set(isbn_list)
        book.save()
        return book
