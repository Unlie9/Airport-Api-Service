from rest_framework import serializers
from airport.models import (
    Airport,
    Route,
    Airplane,
    AirplaneType,
    Crew,
    Order,
    Flight,
    Ticket
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route


