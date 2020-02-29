# from django.contrib.auth.models import AbstractUser
from django.db import models

# import uuid


# class User(AbstractUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Author(models.Model):
    name = models.CharField(max_length=128)


class ISBN(models.Model):
    number = models.CharField(max_length=32, unique=True)


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ManyToManyField(Author)
    publication_date = models.DateField()
    isbn = models.ManyToManyField(ISBN)
    num_of_pages = models.IntegerField()
    link_to_cover = models.URLField(blank=True)
    publication_lang = models.CharField(max_length=32)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['title', 'author', 'isbn'], name="different_isbns")
    #     ]
