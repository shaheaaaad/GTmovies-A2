from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='posters')
    price = models.FloatField()
    release_date = models.DateField()

    def __str__(self):
        return self.title