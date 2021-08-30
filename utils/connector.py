from rest_framework.response import Response
from rest_framework import status

import json
import requests

from movies.models import Movie

api_key = 'bb4cf141'
url = f"http://www.omdbapi.com/?apikey={api_key}&t="

class MovieClass:
    movie_data = {}

    def save_to_database(self):
        m, created = Movie.objects.get_or_create(Data=self.movie_data)
        m.save()
        if created:
            return 201
        else:
            return 400

class APIConnector:
    def __init__(self, q: str):
        self.q = q

    def get_movie_data(self):
        api_request = requests.get(f"{url}{self.q}")
        data = json.loads(api_request.content)
        movie_item = MovieClass()
        movie_item.movie_data = data
        if data['Response'] == 'True':
            return movie_item.save_to_database()
        elif data['Response'] == 'False':
            return 404
        else:
            return 400