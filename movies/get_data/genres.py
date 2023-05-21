import json
import requests

api_key = '479238dda68da66dd672d6ed123ca263'

result = []

genre_data = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ko'
response = requests.get(genre_data).json()
genres = response.get('genres')

for genre in genres:
    genre_dict = {
        'model': 'movies.genre',
        'pk': genre.get('id'),
        'fields': {
            'genre_id': genre.get('id'),
            'name': genre.get('name')
        }
    }
    result.append(genre_dict)

with open('genres.json', 'w', encoding='UTF-8') as file:
    file.write(json.dumps(result, ensure_ascii=False))