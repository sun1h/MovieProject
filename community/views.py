from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse,HttpResponse
from community.models import *
from movies.models import Movie
from .forms import *
from django.views.decorators.http import require_POST

# Create your views here.
@login_required
def index(request):    
    reviews = Review.objects.all().order_by('-pk')

    context = {
        'reviews': reviews,
    }
    
    return render(request, 'community/index.html', context)


def detail(request, review_pk):     # 개별 리뷰 조회 페이지
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm()
    comments = review.comment_set.all()

    movie = review.movie
    genres = movie.genres.all() 

    genre = ''

    for g in genres:
        genre += str(g)
        genre += ' / '
    
    genre = genre[:-3]



    context = {
        'review': review,
        'genre': genre,
        'comment_form': comment_form,
        'comments': comments,

    }
    return render(request, 'community/detail.html', context)


@login_required
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_liked = False
        else:
            review.like_users.add(user)
            is_liked = True

        context = {
            'is_liked': is_liked, 
            'like_count': review.like_users.count(),
        }
        return JsonResponse(context)
    return HttpResponse(status=401)

@login_required
def create(request):        # 리뷰 작성 페이지
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/reviewform.html', context)


@login_required
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user or request.user.is_superuser:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                # review = form.save(commit=False)
                # review.user = request.user
                review.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form
        }
        return render(request, 'community/reviewform.html', context)
    else:
        return redirect('from django.views.decorators.http import require_POST', review.pk)


@login_required
def delete(request, review_pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user or request.user.is_superuser:
            review.delete()
    return redirect('community:index')


@login_required
@require_POST
def comments_create(request,pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review,pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
        return redirect('community:detail',review.pk)
    return redirect('accounts:login')


@login_required
@require_POST
def comments_delete(request, review_pk,comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail',review_pk)
