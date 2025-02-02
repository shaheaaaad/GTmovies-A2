from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    class Meta:
        db_table = "MovieStore_movie"
    def __str__(self):
        return self.title