from decimal import Decimal

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .models import *

fake = Faker()


class ServiceAreaTest(APITestCase):
    def setUp(self):
        provider_data = {
            'name': fake.first_name(),
            'email': fake.email(),
            'language': fake.language_code(),
            'currency': 'USD',
            'phone_number': fake.phone_number()
        }
        self.provider = Provider.objects.create(**provider_data)
        self.service_area_data = {
            'name': fake.name(),
            'price': '135.5',
            'provider_id': self.provider.id,
            'polygon': 'POLYGON(( 10 10, 10 20, 90 90, 25 15, 10 10))'
        }

        self.service_area = ServiceArea.objects.create(
            provider=self.provider, **self.service_area_data)

    def test_create_area(self):
        data = {
            'name': fake.color_name(),
            'price': '89.49',
            'provider_id': self.provider.id,
            'polygon': 'POLYGON(( 30 30, 40 20, 20 20, 20 10, 30 30))'
        }
        response = self.client.post('/service_areas/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_service_area(self):
        response = self.client.get('/service_areas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

    def test_get_service_area_details(self):
        path = f'/service_areas/{self.service_area.id}/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_area(self):
        path = f'/service_areas/{self.service_area.id}/'
        self.service_area_data.update({'price': '100'})
        response = self.client.put(path, self.service_area_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            ServiceArea.objects.get(pk=self.service_area.id).price,
            Decimal('100.00'))

    def test_update_area_patch(self):
        path = f'/service_areas/{self.service_area.id}/'
        data = {'name': 'test'}
        response = self.client.patch(path, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            ServiceArea.objects.get(pk=self.service_area.id).name, 'test')

    def test_get_existent_area(self):
        path = f'/get_areas/?lat={10}&lng={10}'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

    def test_remove_area(self):
        path = f'/service_areas/{self.service_area.id}/'
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProviderTest(APITestCase):
    def setUp(self):
        self.data = {
            'name': 'John Doe',
            'email': 'johndoe@test.com',
            'language': 'pt',
            'currency': 'BRL',
            'phone_number': '+123456789'
        }
        self.provider = Provider.objects.create(**self.data)

    def test_create_provider(self):
        response = self.client.post('/providers/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_providers(self):
        response = self.client.get('/providers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_provider_details(self):
        path = f'/providers/{self.provider.id}/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_provider(self):
        path = f'/providers/{self.provider.id}/'
        self.data.update({'email': 'johndoe@gmail.com'})
        response = self.client.put(path, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Provider.objects.get(pk=self.provider.id).email,
            'johndoe@gmail.com')

    def test_update_provider_patch(self):
        path = f'/providers/{self.provider.id}/'
        data = {'currency': 'USD'}
        response = self.client.patch(path, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Provider.objects.get(pk=self.provider.id).currency, 'USD')

    def test_remove_provider(self):
        path = f'/providers/{self.provider.id}/'
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
