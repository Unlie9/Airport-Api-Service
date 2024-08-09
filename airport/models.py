from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=64, unique=True)
    closest_big_city = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Airports"

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departure_routes")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrival_routes")
    distance = models.IntegerField()

    class Meta:
        verbose_name_plural = "Routes"
        indexes = [
            models.Index(fields=["source", "destination"]),
            models.Index(fields=["distance"]),
        ]

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "AirplaneTypes"

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=64, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Airplanes"

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    @property
    def is_small(self):
        return self.capacity < 60

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Crews"

    def __str__(self):
        return self.first_name + " " + self.last_name

    def clean(self):
        if Crew.objects.filter(first_name=self.first_name, last_name=self.last_name).exists():
            raise ValidationError("This person already exists")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"{str(self.created_at)} - {self.user}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew)

    class Meta:
        verbose_name_plural = "Flights"

    def __str__(self):
        return f"{self.route.source} - {self.route.destination}"

    def clean(self):
        if self.departure_time > self.arrival_time:
            raise ValidationError("departure time cannot be greater than arrival time")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        verbose_name_plural = "Tickets",
        ordering = ["seat"]

    def __str__(self):
        return f"{self.row} - {self.seat} - {self.flight}"

    def clean(self):
        # queryset = Flight.objects.filter(seat=self.seat, row=self.row)
        # if queryset.exists(): # error
        #     raise ValidationError("ticket already exists")

        if not (1 <= self.seat <= self.flight.airplane.seats_in_row):
            raise ValueError(
                f"seat must be in range between 1 and {self.flight.airplane.seats_in_row}"
            )
        if self.row > self.flight.airplane.rows:
            raise ValueError("row cannot be greater than flights airplane rows")

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
