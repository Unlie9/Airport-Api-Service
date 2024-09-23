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
router.register(r"airplane-types", AirPlaneTypeViewSet, basename="airplane-types")
router.register(r"airplanes", AirPlaneViewSet, basename="airplanes")
router.register(r"airports", AirportViewSet, basename="airports")
router.register(r"crew", CrewViewSet, basename="crew")
router.register(r"routes", RouteViewSet, basename="routes")
router.register(r"flights", FlightViewSet, basename="flights")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"tickets", TicketViewSet, basename="tickets")


urlpatterns = router.urls

app_name = "airport"
