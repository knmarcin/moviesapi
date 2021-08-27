from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('__all__')


class GetMovieSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=50)