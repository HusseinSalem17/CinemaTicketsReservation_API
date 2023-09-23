# this is like compiler between views and models (make models format can python understand) (convert models to api (json))
from rest_framework import serializers

from tickets.models import Guest, Movie, Reservation, Post


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "hall", "movie"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["pk", "reservation", "name", "mobile"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["pk", "title", "content", "author", "created_at", "updated_at"]