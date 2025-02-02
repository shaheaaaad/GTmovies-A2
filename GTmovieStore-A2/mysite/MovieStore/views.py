from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Movie

def index(request):
    return HttpResponse("Hello, world. This is the MovieStore index")


def movie_list(request):

    movie_list = Movie.objects.all()


    paginator = Paginator(movie_list, 10)  # Show 10 movies per page
    page_number = request.GET.get('page')  # Get current page from URL query params
    page_obj = paginator.get_page(page_number)  # Get the page object

    # Pass the paginated movies to the template
    return render(request, 'movieStore/movie_list.html', {'page_obj': page_obj})
