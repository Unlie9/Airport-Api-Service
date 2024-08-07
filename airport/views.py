from rest_framework import viewsets

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
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    OrderSerializer,
    FlightSerializer,
    TicketSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    def get_queryset(self):
        return self.queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        return self.queryset


class AirPlaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

    def get_queryset(self):
        return self.queryset


class AirPlaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return self.serializer_class


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def get_queryset(self):
        return self.queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return OrderlistSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        return self.serializer_class


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        return self.queryset
