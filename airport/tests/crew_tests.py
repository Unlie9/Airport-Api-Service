from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from airport.models import Crew

CREW_URL = reverse('airport:crew-list')


def detail_crew_url(crew_id):
    return reverse('airport:crew-detail', args=[crew_id])


def sample_crew(**params):
    defaults = {
        "first_name": "John",
        "last_name": "Doe",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


class CrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        self.client.force_authenticate(self.admin_user)

    def test_create_crew(self):
        payload = {
            "first_name": "Alice",
            "last_name": "Smith",
        }
        res = self.client.post(CREW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Crew.objects.filter(first_name=payload['first_name'], last_name=payload['last_name']).exists())

    def test_update_crew(self):
        crew = sample_crew()

        payload = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        url = detail_crew_url(crew.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        crew.refresh_from_db()
        self.assertEqual(crew.first_name, payload['first_name'])
        self.assertEqual(crew.last_name, payload['last_name'])

    def test_delete_crew(self):
        crew = sample_crew()

        url = detail_crew_url(crew.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Crew.objects.filter(id=crew.id).exists())

    def test_filter_crew_by_first_name(self):
        crew1 = sample_crew(first_name="John")
        crew2 = sample_crew(first_name="Jane")

        res = self.client.get(CREW_URL, {'first_name': 'John'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(crew1.id, [crew['id'] for crew in res.data['results']])
        self.assertNotIn(crew2.id, [crew['id'] for crew in res.data['results']])

    def test_filter_crew_by_last_name(self):
        crew1 = sample_crew(last_name="Doe")
        crew2 = sample_crew(last_name="Smith")

        res = self.client.get(CREW_URL, {'last_name': 'Doe'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(crew1.id, [crew['id'] for crew in res.data['results']])
        self.assertNotIn(crew2.id, [crew['id'] for crew in res.data['results']])
