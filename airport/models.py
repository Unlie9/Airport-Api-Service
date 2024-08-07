from django.conf import settings
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=64, unique=True)
    closest_big_city = models.CharField(max_length=64)


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departure_routes")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrival_routes")
    distance = models.IntegerField()


class AirplaneType(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Airplane(models.Model):
    name = models.CharField(max_length=64, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)


class Crew(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
