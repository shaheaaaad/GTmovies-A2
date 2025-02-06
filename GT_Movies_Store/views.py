from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from GT_Movies_Store.models import Movie
from GT_Movies_Store.forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Movie, Review
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'GT_Movies_Store/base.html')
def home(request):
    movies = Movie.objects.all()

    paginator = Paginator(movies, 50)  # Show 10 movies per page
    page_number = request.GET.get('page')  # Get current page from URL query params
    page_obj = paginator.get_page(page_number)
    return render(request, 'GT_Movies_Store/home.html', {'page_obj': page_obj})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'GT_Movies_Store/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to homepage
    else:
        form = AuthenticationForm()

    return render(request, 'GT_Movies_Store/login.html', {'form': form})
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
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST' and request.user.is_authenticated:
        comment = request.POST.get('comment', '').strip()
        if comment:
            Review.objects.create(
                movie=movie,
                comment=comment,
                user=request.user,
            )

    reviews = movie.reviews.all()  # Use the correct related_name
    return render(request, 'GT_Movies_Store/movie.html', {
        'movie': movie,
        'reviews': reviews,
    })


@login_required
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        if comment:
            Review.objects.create(
                movie=movie,
                user=request.user,
                comment=comment
            )
        return redirect('movie', movie_id=id)@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        if comment:
            review.comment = comment
            review.save()
        return redirect('movie', movie_id=id)

    return render(request, 'GT_Movies_Store/edit_review.html', {'review': review, 'movie': movie})
