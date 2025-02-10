from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

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
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    author = models.CharField(max_length=255, default="Unknown Author")
    comment = models.CharField(max_length=255, default="No comment")
    review = models.TextField()

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username}"



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

class SecurityQuestion(models.Model):
    SECURITY_QUESTIONS = [
        ("pet", "What was the name of your first pet?"),
        ("school", "What was the name of your first school?"),
        ("city", "In what city were you born?"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="security_question")
    question = models.CharField(max_length=50, choices=SECURITY_QUESTIONS)
    answer = models.CharField(max_length=255)  # Will be hashed

    def set_answer(self, raw_answer):
        """Hashes the security answer before saving it."""
        self.answer = make_password(raw_answer)

    def check_answer(self, raw_answer):
        """Checks if the provided answer matches the stored hashed answer."""
        return check_password(raw_answer, self.answer)

    def save(self, *args, **kwargs):
        """Ensures the security answer is always hashed before saving."""
        if not self.answer.startswith("pbkdf2_sha256$"):  # Prevent double hashing
            self.set_answer(self.answer)
        super().save(*args, **kwargs)
