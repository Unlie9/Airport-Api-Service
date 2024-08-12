import uuid
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from airport.models import Route, Airport

ROUTE_URL = reverse('airport:routes-list')


def detail_url(route_id):
    return reverse('airport:routes-detail', args=[route_id])


def unique_name(base_name="Sample Airport"):
    return f"{base_name} {uuid.uuid4()}"


def sample_airport(name=None):
    if name is None:
        name = unique_name()
    return Airport.objects.create(name=name, closest_big_city='Sample City')


def sample_route(**params):
    source = sample_airport(name=unique_name("Source Airport"))
    destination = sample_airport(name=unique_name("Destination Airport"))
    defaults = {
        'source': source,
        'destination': destination,
        'distance': 1000,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


class RouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        self.client.force_authenticate(self.admin_user)

    def test_retrieve_routes(self):
        sample_route()
        sample_route()

        res = self.client.get(ROUTE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_create_route(self):
        source = sample_airport(name=unique_name('Source Airport'))
        destination = sample_airport(name=unique_name('Destination Airport'))
        payload = {
            'source': source.id,
            'destination': destination.id,
            'distance': 1500
        }
        res = self.client.post(ROUTE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        route = Route.objects.get(id=res.data['id'])
        self.assertEqual(route.source.id, payload['source'])
        self.assertEqual(route.destination.id, payload['destination'])
        self.assertEqual(route.distance, payload['distance'])

    def test_update_route(self):
        route = sample_route()

        new_source = sample_airport(name=unique_name('New Source Airport'))
        payload = {
            'source': new_source.id,
            'destination': route.destination.id,
            'distance': 2000
        }
        url = detail_url(route.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        route.refresh_from_db()
        self.assertEqual(route.source.id, payload['source'])
        self.assertEqual(route.destination.id, payload['destination'])
        self.assertEqual(route.distance, payload['distance'])

    def test_delete_route(self):
        route = sample_route()

        url = detail_url(route.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Route.objects.filter(id=route.id).exists())

    def test_filter_routes_by_source(self):
        source1 = sample_airport(name=unique_name('Source Airport 1'))
        source2 = sample_airport(name=unique_name('Source Airport 2'))
        route1 = sample_route(source=source1)
        route2 = sample_route(source=source2)

        res = self.client.get(ROUTE_URL, {'source': source1.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(route1.id, [route['id'] for route in res.data['results']])
        self.assertNotIn(route2.id, [route['id'] for route in res.data['results']])

    def test_filter_routes_by_destination(self):
        destination1 = sample_airport(name=unique_name('Destination Airport 1'))
        destination2 = sample_airport(name=unique_name('Destination Airport 2'))
        route1 = sample_route(destination=destination1)
        route2 = sample_route(destination=destination2)

        res = self.client.get(ROUTE_URL, {'destination': destination1.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(route1.id, [route['id'] for route in res.data['results']])
        self.assertNotIn(route2.id, [route['id'] for route in res.data['results']])
