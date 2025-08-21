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


@pytest.mark.django_db
class TestLoginView:

    def setup_method(self):
        self.url = reverse('login')

        base_user = CustomUser.objects.create_user(
            email="base@test.com",
            password="password123",
        )

    def test_login_user_success(self, api_client):
        data = {
            "email": "base@test.com",
            "password": "password123",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_user_with_unneccessery_fields(self, api_client):        
        data = {
            "email": "base@test.com",
            "password": "password123",
            "phone_number": "79998886655"
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_user_with_wrong_password(self, api_client):
        data = {
            "email": "base@test.com",
            "password": "password13",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 401

    def test_login_user_with_unexisting_email(self, api_client):
        data = {
            "email": "bas@test.com",
            "password": "password123",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 401

    def test_login_user_without_password(self, api_client):
        data = {
            "email": "base@test.com",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 401

    def test_login_user_without_email(self, api_client):
        data = {
            "password": "password123",
        }

        response = api_client.post(self.url, data, format='json')

        assert response.status_code == 401


@pytest.mark.django_db
class TestUserViewSet:

    def setup_method(self):
        self.admin = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass"
        )
        self.user1 = CustomUser.objects.create_user(email="user1@example.com", password="pass1")
        self.user2 = CustomUser.objects.create_user(email="user2@example.com", password="pass2")

    def test_admin_can_list_users(self, api_client):
        url = reverse("customuser-list")
        api_client.force_authenticate(self.admin)

        response = api_client.get(url, format="json")

        assert response.status_code == 200
        assert len(response.data) == 3

    def test_admin_can_retrieve_user(self, api_client):
        url = reverse("customuser-detail", kwargs={"pk": self.user1.pk})
        api_client.force_authenticate(user=self.admin)
        
        response = api_client.get(url, format="json")

        assert response.status_code == 200
        assert response.data["email"] == self.user1.email

    def test_non_admin_cannot_access_user_list(self, api_client):
        url = reverse("customuser-list")
        api_client.force_authenticate(user=self.user1)

        response = api_client.get(url, format="json")

        assert response.status_code == 403

    def test_non_admin_cannot_access_user_detail(self, api_client):
        url = reverse("customuser-detail", kwargs={"pk": self.user1.pk})
        api_client.force_authenticate(user=self.user1)

        response = api_client.get(url, format="json")

        assert response.status_code == 403



@pytest.mark.django_db
class TestMeView:

    def setup_method(self):
        self.url = reverse('auth_me')
        self.user = CustomUser.objects.create_user(
            email="user@example.com",
            password="password123",
            name="Test User",
            phone_number="+1234567890"
        )
        self.user2 = CustomUser.objects.create_user(
            email="user2@example.com",
            password="password123",
            name="User Two"
        )

    def test_me_view_authenticated_user(self, api_client):
        api_client.force_authenticate(user=self.user)

        response = api_client.get(self.url, format="json")

        assert response.status_code == 200
        assert response.data["id"] == self.user.id
        assert response.data["email"] == self.user.email
        assert response.data["name"] == self.user.name
        assert response.data["phone_number"] == self.user.phone_number

    def test_me_view_unauthenticated_user(self, api_client):
        response = api_client.get(self.url, format="json")

        assert response.status_code == 401

    def test_me_view_returns_only_authenticated_user_data(self, api_client):
        api_client.force_authenticate(user=self.user)

        response = api_client.get(self.url, data={"id": self.user2.id}, format="json")

        assert response.status_code == 200
        assert response.data["id"] == self.user.id
        assert response.data["email"] == self.user.email
        assert response.data["name"] == self.user.name
