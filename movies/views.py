from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieSerializer, GetMovieSerializer
from utils.connector import APIConnector


def index(request):
    return HttpResponse("Hello World")

class MoviesViewSet(APIView):

    def get(self, request, *args, **kwargs):

        movies = Movie.objects.all()
        filtered_movies = self.request.query_params.getlist('Director')
        print(filtered_movies)

        if filtered_movies is not None:
            for item in filtered_movies:
                movies = Movie.objects.filter(Data__Director__icontains=item)

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # POST to db
    # def post(self, request, *args, **kwargs):
    #     serializer = MovieSerializer(data=request.data, many=False)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = GetMovieSerializer(data=request.data, many=False)
        if serializer.is_valid():
            q = serializer.data.get("question")
            c = APIConnector(q)
            c.get_movie_data()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)