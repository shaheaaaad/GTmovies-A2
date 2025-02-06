from .models import Movie, Review
from django.contrib import admin

from .models import Movie
admin.site.register(Movie)

from .models import Review
admin.site.register(Review)

from .models import Order
admin.site.register(Order)
