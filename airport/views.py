from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from airport.permissions import (
    IsAdminAllOrAuthenticatedOrReadOnly,
    IsAdminReadOnly,
    IsAdminOrReadOnly
)

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
    # FlightListSerializer,
    # FlightDetailSerializer,
    CreateFlightSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    TicketListSerializer,
    TicketCreateSerializer,
)


class Pagination(PageNumberPagination):
    page_size_query_param = "size"
    max_page_size = 3
    page_size = 3


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser,]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by name",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related("source", "destination")
    serializer_class = RouteSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser,]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["source", "destination"]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RouteListSerializer
        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by source",
            ),
            OpenApiParameter(
                name="destination",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by destination",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class AirPlaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser,]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by name",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class AirPlaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all().select_related("airplane_type")
    serializer_class = AirplaneSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser,]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by name",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["first_name", "last_name"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="first_name",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by first_name",
            ),
            OpenApiParameter(
                name="last_name",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by last_name",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["route__source", "departure_time", "arrival_time"]
    ordering_fields = ["departure_time", "arrival_time"]
    search_fields = ["route", "departure_time", "arrival_time"]

    def get_queryset(self):
        queryset = Flight.objects.select_related(
            "route__source",
            "route__destination",
            "airplane__airplane_type"
        ).prefetch_related("crew")

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return CreateFlightSerializer
        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by source",
            ),
            OpenApiParameter(
                name="destination",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by destination",
            ),
            OpenApiParameter(
                name="departure_time",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by departure_time",
            ),
            OpenApiParameter(
                name="arrival_time",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by arrival_time",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = Pagination
    permission_classes = (IsAdminAllOrAuthenticatedOrReadOnly,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("tickets")

        if self.request.user.is_anonymous:
            return queryset.none()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="created_at",
                type=str,
                required=False,
                location=OpenApiParameter.QUERY,
                description="Filter by created_at",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = Pagination
    permission_classes = (IsAdminReadOnly,)
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
