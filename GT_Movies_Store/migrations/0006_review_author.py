# Generated by Django 5.1.5 on 2025-02-02 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GT_Movies_Store', '0005_movie_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.CharField(default='Unknown Author', max_length=255),
        ),
    ]
