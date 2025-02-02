from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'GT_Movies_Store/base.html')
def home(request):
    return render(request, 'GT_Movies_Store/home.html')