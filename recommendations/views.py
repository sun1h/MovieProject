import pickle
import os
from django.shortcuts import render
from django.conf import settings
from tmdbv3api import Movie, TMDb
from django import forms


movie_data = Movie()
tmdb = TMDb()
tmdb.api_key = '479238dda68da66dd672d6ed123ca263'
tmdb.language = 'ko-KR'

def get_recommendations(title):
    # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
    idx = movies[movies['title'] == title].index[0]

    # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
    sim_scores = sim_scores[1:11]
    
    # 추천 영화 목록 10개의 인덱스 정보 추출
    movie_indices = [i[0] for i in sim_scores]
    
    # 인덱스 정보를 통해 영화 제목 추출
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie_data.details(id)
        
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'

        images.append(image_path)
        titles.append(details['title'])

    return list(zip(images, titles))

movies_pickle_path = os.path.join(settings.BASE_DIR, 'movies.pickle')
cosine_sim_pickle_path = os.path.join(settings.BASE_DIR, 'cosine_sim.pickle')

movies = pickle.load(open(movies_pickle_path, 'rb'))
cosine_sim = pickle.load(open(cosine_sim_pickle_path, 'rb'))

def home(request):
    if request.method == 'POST':
        title = request.POST['title']
        recommendations = get_recommendations(title)
        print(recommendations)
        print('hi')
        context = {
            'recommendations': recommendations
        }
        return render(request, 'recommendations/recommendations.html', context)
    else:
        movie_list = movies['title'].values
        context = {
            'movie_list': movie_list
        }
        return render(request, 'recommendations/home.html', context)
