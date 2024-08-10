from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
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
    RouteListSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    OrderSerializer,
    FlightSerializer,
    TicketSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    CreateFlightSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    TicketListSerializer,
    TicketCreateSerializer,
)


class Pagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 3
    page_size = 3


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    def get_queryset(self):
        return self.queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related("source", "destination")
    serializer_class = RouteSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["source", "destination"]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RouteListSerializer
        return self.serializer_class


class AirPlaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    def get_queryset(self):
        return self.queryset


class AirPlaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all().select_related("airplane_type")
    serializer_class = AirplaneSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["name"]
    ordering_fields = ["rows", "seats_in_row"]

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["first_name", "last_name"]


class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["route__source", "route__destination", "airplane", "departure_time", "arrival_time"]
    ordering_fields = ["departure_time", "arrival_time"]
    search_fields = ["route", "departure_time", "arrival_time"]

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Flight.objects.select_related(
            "route__source",
            "route__destination",
            "airplane__airplane_type",
        ).prefetch_related("crew")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        elif self.action == "create":
            return CreateFlightSerializer
        return self.serializer_class


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related("user")
    serializer_class = OrderSerializer
    pagination_class = Pagination
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ["flight__route__name"]
    search_fields = ["flight__route__name"]

    def get_queryset(self):
        return self.queryset.select_related()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "create":
            return TicketCreateSerializer
        return self.serializer_class
