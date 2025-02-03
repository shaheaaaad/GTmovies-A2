from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)  # ✅ Add this line

    class Meta:
        db_table = "MovieStore_movie"
    def __str__(self):
        return self.title
class Review (models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review = models.TextField()
    author = models.CharField(max_length=255, default='Unknown Author')

    def __str__(self):
        return f"Review for {self.movie.title}"

class Order (models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username} for {self.movie.title} on {self.order_date.strftime('%Y-%m-%d')}"