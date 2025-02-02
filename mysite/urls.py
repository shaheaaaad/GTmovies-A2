"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from GT_Movies_Store import views
from GT_Movies_Store.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('MovieStore/', views.movie_list, name='movie_list'),

    path('cart/', views.cart, name='cart'),

    path('login/', views.login, name='login'),

    path('account/', views.account, name='account'),

    path('welcome/', views.welcome, name='welcome'),

    path('logout/', logout_view, name='logout_view'),

    path("<int:movie_id>/movie/", views.movie, name="movie"),
]
