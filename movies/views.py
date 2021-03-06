from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie, Comment
from movies.serializers import MovieSerializer, GetMovieSerializer, CommentSerializer
from utils.connector import APIConnector
from utils.comment_validator import no_empty_validator


class MoviesViewSet(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Movie.objects.all()

        # List of all available
        filter_keys = [  # List of all available filter keys - it is expandable
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


        # Optional sort. You can choose any field after Data.
        sort_by = self.request.query_params.get('sort')
        if sort_by:
            queryset = queryset.order_by(f"Data__{sort_by}")

        # Default sort is by not nested - id.
        else:
            queryset = queryset.order_by('-id')

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
            check_if_created = c.get_movie_data()
            if check_if_created == 404:
                return Response(data={"Error": "Movie wasn't found on external API"}, status=status.HTTP_404_NOT_FOUND)
            elif check_if_created == 400:
                return Response(data={"Error": "Entry already exists"}, status=status.HTTP_204_NO_CONTENT)
            elif check_if_created == 201:
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        id_filter = self.request.query_params.get('id')
        if id_filter:
            queryset = queryset.filter(movie_id__exact=id_filter)
        serializer = CommentSerializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):

        comment = request.data.get("comment")
        no_empty_validator(comment)

        serializer = CommentSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
