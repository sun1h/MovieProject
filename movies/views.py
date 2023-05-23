from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from dotenv import load_dotenv
from movies.forms import RateForm
from .models import *
from community.models import Review
import os


load_dotenv()
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

# Create your views here.
def index(request):
    
    popular_movies = Movie.objects.all().order_by('-popularity').order_by('?')[:18]
    group_popular_movies = list([popular_movies[:6], popular_movies[6:12], popular_movies[12:]])

    best_movies = Movie.objects.all().order_by('-vote_average').order_by('?')[:18]
    group_best_movies = list([best_movies[:6], best_movies[6:12], best_movies[12:]])

    context = {
        'group_popular_movies': group_popular_movies,
        'group_best_movies': group_best_movies,
    }
    
    return render(request, 'movies/index.html', context)


def all(request):
    movies = Movie.objects.all().order_by('movie_id')

    page = Paginator(movies, 18)
    num = request.GET.get('page')
    page = page.get_page(num)

    context = {
        'movies': movies,
        'page' : page,
    }
    return render(request, 'movies/all.html', context)

def old(request):
    movies = Movie.objects.all().order_by('release_date')
    
    page = Paginator(movies, 18)
    num = request.GET.get('page')
    page = page.get_page(num)
    
    context = {
        'movies': movies,
        'page': page,
    }
    return render(request, 'movies/old.html', context)

def recent(request):
    movies = Movie.objects.all().order_by('-release_date')
    
    page = Paginator(movies, 18)
    num = request.GET.get('page')
    page = page.get_page(num)
    
    context = {
        'movies': movies,
        'page': page,
    }
    return render(request, 'movies/recent.html', context)

def popularity(request):
    movies = Movie.objects.all().order_by('-popularity')
    
    page = Paginator(movies, 18)
    num = request.GET.get('page')
    page = page.get_page(num)
    
    context = {
        'movies': movies,
        'page': page,
    }
    return render(request, 'movies/popularity.html', context)

def top_rate(request):
    movies = Movie.objects.all().order_by('-vote_average')
    
    page = Paginator(movies, 18)
    num = request.GET.get('page')
    page = page.get_page(num)
    
    context = {
        'movies': movies,
        'page': page,
    }
    return render(request, 'movies/top_rate.html', context)

def search(request):
    movies = Movie.objects.all()

    searchword = request.GET.get('searchword', '')

    if searchword:
        result_movies = movies.filter(title__contains=searchword)
    else:
        return redirect('movies:all')
        
    context = {
        'result_movies': result_movies,
        }

    return render(request, 'movies/searchresult.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    genres = movie.genres.all()

    genre = ''

    for text in genres:
        genre += str(text)
        genre += ' / '
    
    genre = genre[:-3]

    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.movie = movie
            rate.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = RateForm()
        rates = Rate.objects.filter(movie=movie)

        total = 0
        for r in rates:
            total += r.star
        if total != 0:
            average = round(total / (len(rates)), 1)
        else:
            average = 0

    lock = 'false'
    for rate in rates:
        if request.user == rate.user:
            lock = 'true'

    context = {
        'movie': movie,
        'genre': genre,
        'form': form,
        'rates': rates,
        'average': average,
        'lock': lock,
    }

    return render(request, 'movies/detail.html', context)


@login_required
def like(request, movie_pk):
    if request.user.is_authenticated:
        user = request.user
        movie = get_object_or_404(Movie, pk=movie_pk)

        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            is_liked = False
        else:
            movie.like_users.add(user)
            is_liked = True
      
        context = {
            'is_liked': is_liked,
            'like_count': movie.like_users.count(),
        }
        return JsonResponse(context)
    return HttpResponse(status=401)
    
@login_required
def delete_rate(request, movie_pk, rate_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = get_object_or_404(Rate, pk=rate_pk)
    if request.user == rate.user and request.method == 'POST':
        rate.delete()
    return redirect('movies:detail', movie.pk)

@login_required
def recommendation(request):
    if request.user.is_authenticated:
        movies = Movie.objects.order_by('?')[:6]
        movie = Movie.objects.order_by('?')[:1]
        action = Movie.objects.filter(genres=28).order_by('?')[:6]
        animation = Movie.objects.filter(genres=16).order_by('?')[:6]
        comedy = Movie.objects.filter(genres=35).order_by('?')[:6]
        fantasy = Movie.objects.filter(genres=14).order_by('?')[:6]
        romance = Movie.objects.filter(genres=10749).order_by('?')[:6]
        
        context = {
            'movies': movies,
            'movie': movie,
            'action': action,
            'animation': animation,
            'comedy': comedy,
            'fantasy': fantasy,
            'romance': romance,
        }

    return render(request,'movies/recommendation.html',context)
