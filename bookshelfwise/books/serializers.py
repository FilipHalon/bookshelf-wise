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
        authors = validated_data.pop("author")
        author_list = []
        for author in authors:
            pk = Author.objects.get_or_create(name=author["name"])[0].id
            author_list.append(pk)
        isbns = validated_data.pop("isbn")
        isbn_list = []
        for isbn in isbns:
            pk = ISBN.objects.get_or_create(number=isbn["number"])[0].id
            isbn_list.append(pk)
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
