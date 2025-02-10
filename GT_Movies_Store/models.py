from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

# ------------------ Movie Model ------------------
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Ensure price exists

    class Meta:
        db_table = "MovieStore_movie"

    def __str__(self):
        return self.title


# ------------------ Review Model ------------------
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    author = models.CharField(max_length=255, default="Unknown Author")
    comment = models.CharField(max_length=255, default="No comment")
    review = models.TextField()

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username}"


# ------------------ Order System ------------------
class Order(models.Model):
    """Stores user purchases"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ Store total

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - ${self.total_price}"

    def calculate_total(self):
        """Recalculate total price from all order items"""
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    """Links movies to orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ Store price at purchase time

    def __str__(self):
        return f"{self.movie.title} (x{self.quantity}) in Order #{self.order.id}"

    @property
    def total_price(self):
        """Calculate total price per item"""
        return self.price * self.quantity


# ------------------ Cart System ------------------
class Cart(models.Model):
    """Shopping cart system"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """Stores items in a cart before checkout"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.movie.title} (x{self.quantity}) in {self.cart.user.username}'s cart"

    @property
    def total_price(self):
        """Calculate total price for cart item"""
        return self.movie.price * self.quantity


# ------------------ Security Question Model ------------------
class SecurityQuestion(models.Model):
    SECURITY_QUESTIONS = [
        ("pet", "What was the name of your first pet?"),
        ("school", "What was the name of your first school?"),
        ("city", "In what city were you born?"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="security_question")
    question = models.CharField(max_length=50, choices=SECURITY_QUESTIONS)
    answer = models.CharField(max_length=255)  # Hashed answer

    def set_answer(self, raw_answer):
        self.answer = make_password(raw_answer)

    def check_answer(self, raw_answer):
        return check_password(raw_answer, self.answer)

    def save(self, *args, **kwargs):
        if not self.answer.startswith("pbkdf2_sha256$"):  # Prevent double hashing
            self.set_answer(self.answer)
        super().save(*args, **kwargs)
