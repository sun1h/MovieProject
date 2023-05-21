import json
import requests

api_key = '479238dda68da66dd672d6ed123ca263'

result = []

for page in range(1, 100):
    movie_data = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={page}'
    
    response = requests.get(movie_data).json()
    movies = response.get('results')
    
    for movie in movies:
        if (movie.get('overview') and movie.get('poster_path')):
            movie_dict = {
                'model': 'movies.movie',
                'pk': movie.get('id'),
                'fields': {
                    'movie_id': movie.get('id'),
                    'title': movie.get('title'),
                    'release_date': movie.get('release_date'),
                    'popularity': movie.get('popularity'),
                    'vote_average': movie.get('vote_average'),
                    'vote_count': movie.get('vote_count'),
                    'overview': movie.get('overview'),
                    'poster_path': movie.get('poster_path'),
                    'backdrop_path': movie.get('backdrop_path'),
                    'genres': movie.get('genre_ids'),
                }
            }
            
            result.append(movie_dict)

with open('movies.json', 'w', encoding='UTF-8') as file:
    file.write(json.dumps(result, ensure_ascii=False))