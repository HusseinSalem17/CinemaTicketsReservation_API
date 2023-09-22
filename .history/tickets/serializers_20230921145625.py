# this is like compiler between views and models (make models format can python understand) (convert models to api (json))
from rest_framework import serializers

from tickets.models import Guest, Movie, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["pk", "reservation", "name", "mobile"]
