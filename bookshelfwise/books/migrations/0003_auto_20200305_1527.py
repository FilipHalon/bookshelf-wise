# Generated by Django 2.2.10 on 2020-03-05 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20200303_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='num_of_pages',
            field=models.IntegerField(verbose_name='page count'),
        ),
    ]