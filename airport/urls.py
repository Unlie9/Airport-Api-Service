from rest_framework import routers
from django.urls import path, include
from airport.views import (
    AirportViewSet,
    RouteViewSet,
    AirPlaneTypeViewSet,
    AirPlaneViewSet
)


router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane_types", AirPlaneTypeViewSet)
router.register("airplanes", AirPlaneViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
