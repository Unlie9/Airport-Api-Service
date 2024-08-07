from rest_framework import routers
from django.urls import path, include
from airport.views import (
    AirportViewSet,
    RouteViewSet,
    AirPlaneTypeViewSet,
    AirPlaneViewSet,
    CrewViewSet,
    OrderViewSet,
    FlightViewSet,
    TicketViewSet
)


router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane_types", AirPlaneTypeViewSet)
router.register("airplanes", AirPlaneViewSet)
router.register("crews", CrewViewSet)
router.register("orders", OrderViewSet)
router.register("flights", FlightViewSet)
router.register("tickets", TicketViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
