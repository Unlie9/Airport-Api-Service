import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from airport.models import AirplaneType, Airplane

AIRPLANE_TYPE_URL = reverse('airport:airplane-types-list')
AIRPLANE_URL = reverse('airport:airplanes-list')


def detail_airplane_type_url(airplane_type_id):
    return reverse('airport:airplane-types-detail', args=[airplane_type_id])


def detail_airplane_url(airplane_id):
    return reverse('airport:airplanes-detail', args=[airplane_id])


def unique_name(base_name="Sample"):
    return f"{base_name} {uuid.uuid4()}"


def sample_airplane_type(**params):
    defaults = {
        "name": unique_name("Airplane Type"),
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    defaults = {
        "name": unique_name("Airplane"),
        "rows": 10,
        "seats_in_row": 6,
        "airplane_type": airplane_type,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


class AirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        self.client.force_authenticate(self.admin_user)

    def test_retrieve_airplane_types(self):
        sample_airplane_type()
        sample_airplane_type()

        res = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_create_airplane_type(self):
        payload = {"name": unique_name("New Airplane Type")}
        res = self.client.post(AIRPLANE_TYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AirplaneType.objects.filter(name=payload['name']).exists())


class AirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        self.client.force_authenticate(self.admin_user)

    def test_retrieve_airplanes(self):
        sample_airplane()
        sample_airplane()

        res = self.client.get(AIRPLANE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)

    def test_create_airplane(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": unique_name("New Airplane"),
            "rows": 15,
            "seats_in_row": 4,
            "airplane_type": airplane_type.id,
        }
        res = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Airplane.objects.filter(name=payload['name']).exists())

    def test_update_airplane(self):
        airplane = sample_airplane()

        payload = {
            "name": unique_name("Updated Airplane"),
            "rows": 20,
            "seats_in_row": 5,
            "airplane_type": airplane.airplane_type.id,
        }
        url = detail_airplane_url(airplane.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        airplane.refresh_from_db()
        self.assertEqual(airplane.name, payload['name'])
        self.assertEqual(airplane.rows, payload['rows'])
        self.assertEqual(airplane.seats_in_row, payload['seats_in_row'])

    def test_delete_airplane(self):
        airplane = sample_airplane()

        url = detail_airplane_url(airplane.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Airplane.objects.filter(id=airplane.id).exists())

    def test_filter_airplanes_by_name(self):
        airplane1 = sample_airplane(name=unique_name("Airplane 1"))
        airplane2 = sample_airplane(name=unique_name("Airplane 2"))

        res = self.client.get(AIRPLANE_URL, {'name': airplane1.name})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(airplane1.id, [airplane['id'] for airplane in res.data['results']])
        self.assertNotIn(airplane2.id, [airplane['id'] for airplane in res.data['results']])