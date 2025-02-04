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
from django.urls import path, include

from GT_Movies_Store import views
from GT_Movies_Store.views import register, login_view, logout_view

from django.contrib.auth import views as auth_views

from GT_Movies_Store.views import setup_security_question

from GT_Movies_Store.views import security_question_reset



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('GT_Movies_Store.urls')),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('MovieStore/', views.movie_list, name='movie_list'),

    path('cart/', views.cart, name='cart'),

    path('login/', views.login_view, name='login'),
    path('register/', register, name='register'),

    path('account/', views.account, name='account'),

    path('welcome/', views.welcome, name='welcome'),

    path('logout/', logout_view, name='logout_view'),

    path("<int:movie_id>/movie/", views.movie, name="movie"),

    path('setup_security_question/', setup_security_question, name='setup_security_question'),
    path('reset_password_security/', security_question_reset, name='security_question_reset'),

]
