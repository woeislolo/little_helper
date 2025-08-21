from django.urls import reverse

import pytest

from users.models import *


@pytest.mark.django_db
class TestRegisterView:

    def setup_method(self):
        self.url = reverse('register')

        base_user = CustomUser.objects.create(
            email="base@test.com",
            password="password123",
        )

    def test_register_user_success(self, api_client):
        data = {
            "email": "test@test.com",
            "password": "password123",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 201
        assert CustomUser.objects.filter(email="test@test.com").exists()

    def test_register_user_with_existing_email(self, api_client):
        data = {
            "email": "base@test.com",
            "password": "password123",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'email' in response.data

    def test_register_user_with_short_password(self, api_client):
        data = {
            "email": "test@test.com",
            "password": "pass123",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'password' in response.data

    def test_register_user_without_email(self, api_client):
        data = {
            "password": "password123",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'email' in response.data

    def test_register_user_without_password(self, api_client):
        data = {
            "email": "test@test.com",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'password' in response.data

    def test_register_user_with_unneccessery_fields(self, api_client):
        data = {
            "email": "base@test.com",
            "password": "pass123",
            "phone_number": "79998886655"
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 400
