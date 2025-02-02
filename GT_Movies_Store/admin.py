from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Movie

admin.site.register(Movie)

from .models import Review

admin.site.register(Review)
