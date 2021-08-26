from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view

from movies.models import Movie
from movies.serializers import MovieSerializer


def index(request):
    return HttpResponse("Hello World")

class MoviesViewSet(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

