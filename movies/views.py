from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from dotenv import load_dotenv
from movies.forms import RateForm
from .models import *
from community.models import Review
import random, requests, os
from embed_video.admin import AdminVideoMixin

load_dotenv()
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

# Create your views here.
def index(request):
    
    if request.user.is_authenticated:
        my_reviews = Review.objects.filter(user_id=request.user.id)
        my_movies = []

        for i in range(len(my_reviews)):
            my_movies.append(Movie.objects.get(pk=my_reviews[i].movie_id))
        
        print_my_movies = my_movies[:6]
    else:
        print_my_movies = []
        
        
    popular_movies = Movie.objects.all().order_by('-popularity')[:6]

    best_movies = Movie.objects.all().order_by('-vote_average')[:6]

    context = {
        'print_my_movies': print_my_movies,
        'popular_movies': popular_movies,
        'best_movies': best_movies,
    }
    
    return render(request, 'movies/index.html', context)


def all(request):
    movies = Movie.objects.all().order_by('id')

    page = Paginator(movies, 12)
    num = request.GET.get('page')
    page = page.get_page(num)

    context = {
        'movies': movies,
        'page' : page,
    }
    return render(request, 'movies/all.html', context)


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

    for g in genres:
        genre += str(g)
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


# def recommendation(request,):
#     fruit_list = ["귤","딸기","사과","감","바나나","파인애플","구아바", "복숭아", "망고스틴"]
#     hate = ["사과","구아바"]
#     context = {
#         'fruit_name' : fruit_list,
#         'hate' : hate,
#     }
#     return render(request,'movies/recommendation.html',context)


def recommendation(request,):
    movie = Movie.objects.order_by('?')[:1]
    context={
        'movie':movie
    }
    return render(request,'movies/recommendation.html',context)
