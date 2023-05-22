# from django.contrib import messages (alert 기능 사용하고싶을때)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import CustomUserChangeForm, CustomUserCreationForm

from community.models import Review, Movie

# Create your views here.

# 회원가입
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


# 로그인
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


# 로그아웃

def logout(request):
    auth_logout(request)
    return redirect('movies:index')


# 회원탈퇴
@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('movies:index')


# 회원정보 수정
@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


# 비밀번호 변경
@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)    # 비밀번호 변경시 로그아웃 방지
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


# 프로필 페이지
@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)

    

    context = {
        'person': person,
    }

    return render(request, 'accounts/profile.html', context)

    # likes = list(person.like_movies.all())[:12]
    # genre_print = ''
    # genres = {}
    # for like in likes:
    #     genre = like.genres.all()
    #     for g in genre:
    #         if g not in genres:
    #             genres[g] = 1
    #         else:
    #             genres[g] += 1

    # if len(genres) >= 5:
    #     print_genres = sorted(genres.items(), key = lambda item: item[1], reverse=True)
    
    # #     for i in range(5):
    # #         genre_print += str(print_genres[i][0]) + ' / '
    

    # #     genre_print = genre_print[:-3]

    # # reviews = Review.objects.filter(user_id=person.id)
    # # reviewed_movies = [[0, 'title'] for x in range(len(reviews))]

    # # for i in range(len(reviews)):
    # #     reviewed_movies[i][0] = reviews[i].pk
    # #     reviewed_movies[i][1] = Movie.objects.get(pk=reviews[i].movie_id)

    # # reviewed_movies = reviewed_movies[:12]
        
    # # context = {
    # #     'person': person,
    # #     'reviewed_movies': reviewed_movies,
    # #     'likes': likes,
    # #     'genre_print': genre_print,
    # # }
    # # return render(request, 'accounts/profile.html', context)

# @login_required
# @require_POST
# def follow(request, user_pk):
#     print('hi')
#     if request.user.is_authenticated:
#         person = get_object_or_404(get_user_model(), pk=user_pk)
#         print(person)
#         print('hi')
#         user = request.user

#         if person != user:
#             if person.followers.filter(pk=user.pk).exists():
#                 person.followers.remove(user)
#                 is_followed = False
#             else:
#                 person.followers.add(user)
#                 is_followed = True
#             context = {
#                 'is_followed': is_followed,
#                 'followers_count': person.followers.count(),
#                 'followings_count': person.followings.count(),
#             }
#             return JsonResponse(context)
#         return redirect('accounts:profile', person.username)
#     return redirect('accoutns:login')

@require_POST
def follow(request, username):
    if request.user.is_authenticated:
        User=get_user_model()
        person=User.objects.get(username=username)
        if person != request.user:
            if person.followers.filter(username=request.user).exists():
                person.followers.remove(request.user)
            else:
                person.followers.add(request.user)
        return redirect('accounts:profile', person.username)
    return redirect('accounts:login')
