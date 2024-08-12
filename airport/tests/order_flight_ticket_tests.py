from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
import uuid

from airport.models import (
    Order,
    Flight,
    Route,
    Airplane,
    Crew,
    Ticket,
    Airport,
    AirplaneType
)

ORDER_URL = reverse('airport:orders-list')
TICKET_URL = reverse('airport:tickets-list')
FLIGHT_URL = reverse('airport:flights-list')


def detail_order_url(order_id):
    return reverse('airport:orders-detail', args=[order_id])


def detail_ticket_url(ticket_id):
    return reverse('airport:tickets-detail', args=[ticket_id])


def detail_flight_url(flight_id):
    return reverse('airport:flights-detail', args=[flight_id])


def unique_name(base_name="Sample"):
    return f"{base_name} {uuid.uuid4()}"


def sample_airport(**params):
    defaults = {"name": unique_name("Airport"), "closest_big_city": "Sample City"}
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport(name=unique_name("Source Airport"))
    destination = sample_airport(name=unique_name("Destination Airport"))
    defaults = {"source": source, "destination": destination, "distance": 1000}
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {"name": unique_name("Airplane Type")}
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    defaults = {"name": unique_name("Airplane"), "rows": 10, "seats_in_row": 6, "airplane_type": airplane_type}
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_crew(**params):
    defaults = {"first_name": unique_name("John"), "last_name": unique_name("Doe")}
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_flight(**params):
    airplane = sample_airplane()
    route = sample_route()
    defaults = {
        "departure_time": timezone.now() + timezone.timedelta(hours=1),
        "arrival_time": timezone.now() + timezone.timedelta(hours=2),
        "airplane": airplane,
        "route": route,
    }
    defaults.update(params)
    flight = Flight.objects.create(**defaults)
    flight.crew.add(sample_crew())
    return flight


class OrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='user',
            email='user@test.com',
            password='testpass'
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )

    def test_create_order_authenticated(self):
        self.client.force_authenticate(self.user)
        flight = sample_flight()

        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.id,
                }
            ]
        }

        res = self.client.post(ORDER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED, msg=res.data)
        self.assertTrue(Order.objects.filter(id=res.data['id']).exists())

    def test_retrieve_orders_authenticated(self):
        self.client.force_authenticate(self.user)
        Order.objects.create(user=self.user)
        Order.objects.create(user=self.user)

        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_retrieve_orders_unauthenticated(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class FlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='user',
            email='user@test.com',
            password='testpass'
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )

    def test_retrieve_flights_authenticated(self):
        self.client.force_authenticate(self.user)
        sample_flight()
        sample_flight()

        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_create_flight_admin(self):
        self.client.force_authenticate(self.admin_user)
        route = sample_route()
        airplane = sample_airplane()
        crew_member = sample_crew()

        print("Route ID:", route.id)
        print("Airplane ID:", airplane.id, "Airplane Name:", airplane.name)
        print("Crew Member ID:", crew_member.id)

        departure_time = timezone.now() + timezone.timedelta(hours=1)
        arrival_time = departure_time + timezone.timedelta(hours=2)

        payload = {
            "route": route.id,
            "airplane": airplane.name,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "crew": [crew_member.id],
        }

        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED, msg=res.data)
        self.assertTrue(Flight.objects.filter(id=res.data['id']).exists())

    def test_create_flight_non_admin(self):
        self.client.force_authenticate(self.user)
        route = sample_route()
        airplane = sample_airplane()
        crew_member = sample_crew()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": timezone.now() + timezone.timedelta(hours=1),
            "arrival_time": timezone.now() + timezone.timedelta(hours=2),
            "crew": [crew_member.id],
        }
        res = self.client.post(FLIGHT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TicketApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        self.user = get_user_model().objects.create_user(
            username='user',
            email='user@test.com',
            password='testpass'
        )

    def test_retrieve_tickets_admin(self):
        self.client.force_authenticate(self.admin_user)
        order = Order.objects.create(user=self.admin_user)
        Ticket.objects.create(row=1, seat=1, flight=sample_flight(), order=order)
        Ticket.objects.create(row=2, seat=2, flight=sample_flight(), order=order)

        res = self.client.get(TICKET_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_create_ticket_non_admin(self):
        self.client.force_authenticate(self.user)
        order = Order.objects.create(user=self.user)
        flight = sample_flight()
        payload = {"row": 1, "seat": 1, "flight": flight.id, "order": order.id}
        res = self.client.post(TICKET_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_ticket_non_admin(self):
        self.client.force_authenticate(self.user)
        order = Order.objects.create
