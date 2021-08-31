from django.db import models


class Movie(models.Model):
    Data = models.JSONField()


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.CharField(max_length=280)
