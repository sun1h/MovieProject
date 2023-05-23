from django.urls import path
from . import views
from movies import views
app_name = 'movies'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.index, name='index'),
    path('all/', views.all, name='all'),
    path('all/old/', views.old, name='old'),
    path('all/recent/', views.recent, name='recent'),
    path('all/popularity/', views.popularity, name='popularity'),
    path('all/top_rate/', views.top_rate, name="top_rate"),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/<int:rate_pk>/delete/', views.delete_rate, name='delete_rate'),
    path('recommendation/', views.recommendation, name='recommendation'),
]