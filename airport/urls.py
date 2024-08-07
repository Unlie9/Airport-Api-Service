from django.urls import path, include
from airport.views import AirportViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register("airports", AirportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
