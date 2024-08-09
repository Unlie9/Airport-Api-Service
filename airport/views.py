from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

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
    AirplaneDetailSerializer, TicketListSerializer, TicketCreateSerializer,
)


class Pagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 4
    page_size = 4


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return self.queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return self.queryset


class AirPlaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return self.queryset


class AirPlaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    pagination_class = Pagination

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
    pagination_class = Pagination


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    pagination_class = Pagination

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        return self.serializer_class


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return self.queryset

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "create":
            return TicketCreateSerializer
        return self.serializer_class
