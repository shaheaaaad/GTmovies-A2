from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from GT_Movies_Store.models import Movie


# Create your views here.
def index(request):
    return render(request, 'GT_Movies_Store/base.html')
def home(request):
    return render(request, 'GT_Movies_Store/home.html')
def login_view(request):
    return render(request, 'GT_Movies_Store/login.html')
def about(request):
    return render(request, 'GT_Movies_Store/about.html')
def welcome(request):
    return render(request, 'GT_Movies_Store/welcome.html')

def movie_list(request):

    movies = Movie.objects.all()


    paginator = Paginator(movies, 10)  # Show 10 movies per page
    page_number = request.GET.get('page')  # Get current page from URL query params
    page_obj = paginator.get_page(page_number)  # Get the page object

    # Pass the paginated movies to the template
    return render(request, 'GT_Movies_Store/movie_list.html', {'page_obj': page_obj})
@login_required(login_url='/login/')
def cart(request):
    return render(request, 'GT_Movies_Store/cart.html')

@login_required(login_url='/login/')
def account(request):
    return render(request, 'GT_Movies_Store/account.html')

def logout_view(request):
    logout(request)
    return redirect('/home')

def movie(request, movie_id):
    highlighted_movie = get_object_or_404(Movie, id=movie_id)
    return render(request, "GT_Movies_Store/movie.html", {"movie": highlighted_movie})
