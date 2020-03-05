from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


class ISBN(models.Model):
    number = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.number}"


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ManyToManyField(Author)
    publication_date = models.DateField()
    isbn = models.ManyToManyField(ISBN)
    num_of_pages = models.IntegerField(verbose_name="page count")
    link_to_cover = models.URLField(blank=True)
    publication_lang = models.CharField(
        max_length=32, verbose_name="publication language"
    )

    def __str__(self):
        return f"{self.title}"

    @staticmethod
    def get_m2m_id_list(data_source, data, model_name):
        input_list = []
        if data_source == "filter_form":
            input_list = "".join(data.get(model_name)).split(", ")
        elif data_source == "serializer":
            input_list = data.pop(model_name)[0].values()
        id_list = []
        for item in input_list:
            new_obj = ""
            if model_name == "author":
                new_obj = Author.objects.get_or_create(name=item)[0]
            elif model_name == "isbn":
                new_obj = ISBN.objects.get_or_create(number=item)[0]
            id_list.append(new_obj)
        return id_list
