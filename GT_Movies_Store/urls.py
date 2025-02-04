from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]