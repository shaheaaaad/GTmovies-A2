from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from GT_Movies_Store.models import Movie


# Create your views here.
def index(request):
    return render(request, 'GT_Movies_Store/base.html')
def home(request):
    return render(request, 'GT_Movies_Store/home.html')

def movie_list(request):

    movies = Movie.objects.all()


    paginator = Paginator(movies, 10)  # Show 10 movies per page
    page_number = request.GET.get('page')  # Get current page from URL query params
    page_obj = paginator.get_page(page_number)  # Get the page object

    # Pass the paginated movies to the template
    return render(request, 'GT_Movies_Store/movie_list.html', {'page_obj': page_obj})