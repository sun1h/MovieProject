from django.urls import path
from . import views
from movies import views
app_name = 'movies'

urlpatterns = [
    path('search/', views.search, name='search'),    
    path('', views.index, name='index'),    
    path('all/', views.all, name='all'),   
    path('<int:movie_pk>/', views.detail, name='detail'),   
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/<int:rate_pk>/delete/', views.delete_rate, name='delete_rate'), 
    path('recommendation/', views.recommendation, name='recommendation'),   
]