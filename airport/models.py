from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


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

    @property
    def get_info(self):
        return str(self)


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
        return "Yes" if self.capacity < 60 else "No"

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
        indexes = [
            models.Index(fields=["route", "airplane"]),
            models.Index(fields=["departure_time"]),
            models.Index(fields=["arrival_time"]),
        ]

    def __str__(self):
        return f"{self.route.source} - {self.route.destination}"

    @property
    def get_route(self):
        return str(self)

    @staticmethod
    def validate_departure_and_arrival_time(departure_time, arrival_time, error_to_raise):
        if departure_time > arrival_time:
            raise error_to_raise(
                {
                    "departure_time": "departure time can't be later than arrival_time",
                }
            )

    @staticmethod
    def validate_departure_and_now_time(departure_time, now_time, error_to_raise):
        if departure_time < now_time:
            raise error_to_raise(
                {
                    "departure_time": "departure time can't be earlier than now",
                }
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        verbose_name_plural = "Tickets"
        ordering = ["seat"]
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "flight"], name="unique_ticket_seat_row_flight"
            )
        ]

    @staticmethod
    def validate_seat(seat, seats_in_row, error_to_raise):
        if not (1 <= seat <= seats_in_row):
            raise error_to_raise(
                {
                    "seat": f"seat must be in range between 1 "
                            f"and airplane seats in row: {seats_in_row}"
                }
            )

    @staticmethod
    def validate_row(row, rows, error_to_raise):
        if not row <= rows:
            raise error_to_raise(
                {
                    "row": f"row cannot be greater than flights airplane rows: {rows}"
                }
            )
        if not 1 <= row:
            raise error_to_raise(
                {
                    "row": f"row cannot be lower than 1"
                }
            )

    def clean(self):
        Ticket.validate_seat(self.seat, self.flight.airplane.seats_in_row, ValueError)
        Ticket.validate_row(self.row, self.flight.airplane.rows, ValueError)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
