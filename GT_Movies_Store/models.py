from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ Add this line

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

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    movies = models.ManyToManyField(Movie, through='OrderItem')  # OrderItems will store individual movies

    def __str__(self):
        return f"Order by {self.user.username} on {self.order_date.strftime('%Y-%m-%d')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.movie.title} (x{self.quantity}) in Order #{self.order.id}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.movie.title} (x{self.quantity}) in {self.cart.user.username}'s cart"

    @property
    def total_price(self):
        # Assuming the Movie model has a price field (add it if necessary)
        return self.movie.price * self.quantity if hasattr(self.movie, 'price') else 0

