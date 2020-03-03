from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ISBN(models.Model):
    number = models.CharField(max_length=32)

    def __str__(self):
        return self.number


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ManyToManyField(Author)
    publication_date = models.DateField()
    isbn = models.ManyToManyField(ISBN)
    num_of_pages = models.IntegerField()
    link_to_cover = models.URLField(blank=True)
    publication_lang = models.CharField(max_length=32, verbose_name="publication language")

    def __str__(self):
        return self.title

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['title', 'author', 'isbn'], name="different_isbns")
    #     ]
