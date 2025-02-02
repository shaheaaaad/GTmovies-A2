from django.urls import path
from . import views

urlpatterns = [
    path('MovieStore/', views.movie_list, name='movie_list'),
]