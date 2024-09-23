from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from airport.models import Airport

AIRPORT_URL = reverse('airport:airports-list')


class AirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        self.client.force_authenticate(self.admin_user)

    def test_retrieve_airports(self):
        Airport.objects.create(name='Airport 1', closest_big_city='City 1')
        Airport.objects.create(name='Airport 2', closest_big_city='City 2')

        res = self.client.get(AIRPORT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_create_airport(self):
        payload = {'name': 'New Airport', 'closest_big_city': 'New City'}
        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Airport.objects.filter(name='New Airport').exists())
