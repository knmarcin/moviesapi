from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieSerializer


def index(request):
    return HttpResponse("Hello World")

class MoviesViewSet(APIView):

    def get(self, *args, **kwargs):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

