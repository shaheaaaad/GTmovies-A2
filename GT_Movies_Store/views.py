import re

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from GT_Movies_Store.models import Movie, Cart, CartItem, SecurityQuestion
from GT_Movies_Store.forms import UserRegistrationForm, SecurityQuestionForm


# --------------------------- General Views ---------------------------

def index(request):
    return render(request, 'GT_Movies_Store/base.html')


def home(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 50)  # Show 50 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'GT_Movies_Store/home.html', {'page_obj': page_obj})


def about(request):
    return render(request, 'GT_Movies_Store/about.html')


def welcome(request):
    return render(request, 'GT_Movies_Store/welcome.html')


# --------------------------- Authentication Views ---------------------------

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
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'GT_Movies_Store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/home')


# --------------------------- Movie Views ---------------------------

def movie_list(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)  # Show 10 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'GT_Movies_Store/movie_list.html', {'page_obj': page_obj})


def movie(request, movie_id):
    highlighted_movie = get_object_or_404(Movie, id=movie_id)
    return render(request, "GT_Movies_Store/movie.html", {"movie": highlighted_movie})


# --------------------------- Cart Views ---------------------------

@login_required(login_url='/login/')
def account(request):
    return render(request, 'GT_Movies_Store/account.html')
@login_required(login_url='/login/')
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    cart_total = sum(item.total_price for item in cart_items)

    return render(request, 'GT_Movies_Store/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


@login_required(login_url='/login/')
def add_to_cart(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, movie=movie)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return render(request, 'GT_Movies_Store/movie.html', {
        'movie': movie,
        'success_message': 'Item added to cart successfully!'
    })


@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


# --------------------------- Security Question Setup ---------------------------

@login_required
def setup_security_question(request):
    """Allows users to set up or update their security question."""
    try:
        security_question = SecurityQuestion.objects.get(user=request.user)
    except SecurityQuestion.DoesNotExist:
        security_question = None

    if request.method == "POST":
        form = SecurityQuestionForm(request.POST, instance=security_question)
        if form.is_valid():
            security_question = form.save(commit=False)
            security_question.user = request.user
            security_question.set_answer(form.cleaned_data["answer"])  # Hash the answer
            security_question.save()
            return redirect("account")
    else:
        form = SecurityQuestionForm(instance=security_question)

    return render(request, "GT_Movies_Store/setup_security_question.html", {"form": form})


# --------------------------- Password Reset Using Security Question ---------------------------

def security_question_reset(request):
    """Resets password using security questions instead of email."""
    if request.method == "POST":
        username = request.POST.get("username")
        security_answer = request.POST.get("security_answer")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(username=username)
            security_question = SecurityQuestion.objects.get(user=user)

            if security_question.check_answer(security_answer):  # Verifies hashed answer
                user.set_password(new_password)  # Updates password securely
                user.save()
                messages.success(request, "Password updated successfully! You can now log in.")
                return redirect("login")
            else:
                messages.error(request, "Incorrect security answer.")
        except (User.DoesNotExist, SecurityQuestion.DoesNotExist):
            messages.error(request, "User or security question not found.")

    return render(request, "GT_Movies_Store/security_question_reset.html")

def search_movies(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, 'GT_Movies_Store/search_results.html', {'movies': [], 'query': query})

    # ✅ Step 1: Prioritize exact title matches
    title_exact_matches = Movie.objects.filter(title__iexact=query).order_by('title')

    # ✅ Step 2: Find full-word matches using regex (prevents "Wheat" from matching "Heat")
    title_regex_matches = Movie.objects.filter(
        Q(title__iregex=fr"\b{re.escape(query)}\b") & ~Q(id__in=title_exact_matches)
    ).order_by('title')

    # ✅ Step 3: Get description matches only if not found in title
    description_matches = Movie.objects.filter(
        Q(description__iregex=fr"\b{re.escape(query)}\b") &
        ~Q(id__in=title_exact_matches.values_list('id', flat=True)) &
        ~Q(id__in=title_regex_matches.values_list('id', flat=True))
    ).order_by('title')

    # Combine results: exact title matches first, then full-word matches, then description matches
    movies = list(title_exact_matches) + list(title_regex_matches) + list(description_matches)

    return render(request, 'GT_Movies_Store/search_results.html', {'movies': movies, 'query': query})