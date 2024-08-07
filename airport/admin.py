from django.contrib import admin
from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Order,
    Flight,
    Ticket
)

admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Crew)
admin.site.register(Order)
admin.site.register(Flight)
admin.site.register(Ticket)
