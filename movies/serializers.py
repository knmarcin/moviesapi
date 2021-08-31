from rest_framework import serializers
from movies.models import Movie, Comment

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('__all__')


class GetMovieSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=50)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment', 'movie_id')