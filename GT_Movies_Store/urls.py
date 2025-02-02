from . import views
from django.urls import path
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),

]