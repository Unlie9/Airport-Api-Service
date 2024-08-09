from django.utils import timezone
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
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "get_info", "distance")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "capacity", "is_small", "airplane_type")


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class FlightSerializer(serializers.ModelSerializer):
    route_info = serializers.CharField(
        source="route.get_info",
        read_only=True,
    )
    airplane = AirplaneListSerializer(many=False, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route_info", "airplane", "departure_time", "arrival_time", "crew")





class CreateFlightSerializer(serializers.ModelSerializer):
    airplane = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airplane.objects.all()
    )
    # route = serializers.SlugRelatedField(
    #     slug_field="get_info",
    #     queryset=Route.objects.all()
    # )

    class Meta:
        model = Flight
        fields = ("id", "departure_time", "arrival_time", "crew", "airplane")

    def validate(self, attrs):
        Flight.validate_departure_and_arrival_time(
            attrs["departure_time"],
            attrs["arrival_time"],
            serializers.ValidationError
        )
        Flight.validate_departure_and_now_time(
            attrs["departure_time"],
            timezone.now(),
            serializers.ValidationError
        )
        return attrs


class FlightListSerializer(FlightSerializer):
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )
    route_info = serializers.CharField(
        source="route.get_info",
        read_only=True,
    )

    class Meta:
        model = Flight
        fields = FlightSerializer.Meta.fields + ("route_info",)


class FlightDetailSerializer(FlightSerializer):
    crew = CrewSerializer(many=True, read_only=True)
    route_info = serializers.CharField(
        source="route.get_info",
        read_only=True,
    )

    class Meta:
        model = Flight
        fields = FlightSerializer.Meta.fields + ("crew", "route_info")


class TicketSerializer(serializers.ModelSerializer):
    flight = serializers.CharField(
        source="flight.route.get_info",
    )

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")

    def validate(self, attrs):
        Ticket.validate_seat(
            attrs["seat"],
            attrs["flight"].airplane.seats_in_row,
            serializers.ValidationError
        )
        Ticket.validate_row(
            attrs["row"],
            attrs["flight"].airplane.rows,
            serializers.ValidationError
        )
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"],
            serializers.ValidationError

        )

        return attrs


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class TicketListSerializer(serializers.ModelSerializer):
    flight = FlightDetailSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "seat", "row", "flight")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "tickets",
            "created_at"
        ]

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(
            **validated_data,
            user=self.context["request"].user
        )

        for ticket_data in tickets_data:
            ticket = Ticket.objects.create(order=order, **ticket_data)
            ticket.save()

        return order
