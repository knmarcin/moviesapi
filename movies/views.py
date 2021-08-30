from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieSerializer, GetMovieSerializer
from utils.connector import APIConnector


def index(request):
    return HttpResponse("Hello World")


class MoviesViewSet(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Movie.objects.all()

        # List of all available
        filter_keys = [ # List of all available filter keys - it is expandable
            'Director',
            'Rated',
            'Year',
            'Genre',
            'Title',
        ]
        filter = {}

        # Loop going through filter_keys list, checking if they are used as query_params
        # If so, it gets all the values and start filtering step by step.
        for key in filter_keys:
            # filter_list is a list of values used by certain key
            # There is possibility of having two or more same query_params
            # ex. ?Director=Peter&Director=Jackson
            filter_list = self.request.query_params.getlist(key)
            if filter_list:
                # For loop going through all the values for certain key and filtering it one by one.
                for item in filter_list:
                    # creating dictionary, then using it for filtering
                    filter[f"Data__{key}__icontains"] = item
                    queryset = queryset.filter(**filter)

        serializer = MovieSerializer(queryset, many=True)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):
        serializer = GetMovieSerializer(data=request.data, many=False)
        if serializer.is_valid():
            q = serializer.data.get("question")
            c = APIConnector(q)
            c.get_movie_data()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
