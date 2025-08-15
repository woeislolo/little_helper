from django.urls import reverse

import pytest

from users.models import *
from help_requests.serializers import *
from help_requests.models import *
from help_requests.urls import *

from tests.factories import UserFactory


@pytest.fixture
def help_request(db):
    author = UserFactory()

    return HelpRequest.objects.create(
        author=author,
        title='Тестовый запрос',
        description='Тестовое описание',
        topic='chat',
        urgency=1
    )

@pytest.mark.django_db
class TestHelpRequestListCreateView:

    def setup_method(self):
        self.url_list_create = reverse('request-list-create')

    def test_get_requests_unauthenticated_forbidden(self, api_client):
        response = api_client.get(self.url_list_create)
        assert response.status_code == 401

    def test_get_requests_authenticated_success(self, auth_client, help_request):
        response = auth_client.get(self.url_list_create)
        assert response.status_code == 200
        assert response.data[0]['title'] == help_request.title

    def test_create_request_authenticated_success(self, auth_client):
        data = {
            'author': 1,
            'title': 'Тестовый запрос 3', 
            'topic': 'chat', 
            'description': 'Здесь описание того, что надо выполнить', 
            'urgency': 1
            }
        response = auth_client.post(
            self.url_list_create, 
            data=data,
            format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'Тестовый запрос 3'

    def test_create_request_authenticated_without_description(self, auth_client):
        data = {
            'author': 1,
            'title': 'Тестовый запрос 3', 
            'topic': 'chat',
            'urgency': 1
            }
        response = auth_client.post(
            self.url_list_create, 
            data=data,
            format='json')
        assert response.status_code == 400

    def test_create_request_unauthenticated_forbidden(self, api_client):
        data = {
            'author': 1,
            'title': 'Тестовый запрос 4', 
            'topic': 'chat', 
            'description': 'Здесь описание того, что надо выполнить', 
            'urgency': 1
            }
        response = api_client.post(
            self.url_list_create, 
            data=data,
            format='json')
        assert response.status_code == 401


@pytest.mark.django_db
class TestHelpRequestRetrieveUpdateDestroyView:

    def setup_method(self):
        pass

    def test_get_request_authenticated_success(self, auth_client, help_request):
        url = reverse('request-detail', kwargs={'pk': help_request.pk})
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.data['title'] == help_request.title

    def test_get_request_authenticated_not_found(self, auth_client):
        url = reverse('request-detail', kwargs={'pk': 999})
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_get_request_unauthenticated(self, api_client, help_request):
        url = reverse('request-detail', kwargs={'pk': help_request.pk})
        response = api_client.get(url)
        assert response.status_code == 401


    def test_update_request_author_success(self, api_client, help_request):
        api_client.force_authenticate(help_request.author)
        url = reverse('request-detail', kwargs={'pk': help_request.pk})
        data = {
            'title': 'Обновлённый заголовок',
            'description': 'Новое описание',
            'topic': help_request.topic,
            'urgency': help_request.urgency
        }

        response = api_client.put(url, data, content_type='application/json')
        help_request.refresh_from_db()

        assert response.status_code == 200
        assert help_request.description == 'Новое описание'

    def test_update_request_author_without_description(self, api_client, help_request):
        api_client.force_authenticate(help_request.author)
        url = reverse('request-detail', kwargs={'pk': help_request.pk})
        data = {
            'title': 'Обновлённый заголовок',
            'topic': help_request.topic,
            'urgency': help_request.urgency
        }

        response = api_client.put(url, data, content_type='application/json')
        help_request.refresh_from_db()

        assert response.status_code == 400

    def test_update_request_not_author_forbidden(self, api_client, help_request, django_user_model):
        not_author =  django_user_model.objects.create_user(email='wrong@wrong.com', password='12345')
        api_client.force_authenticate(not_author)
        url = reverse('request-detail', kwargs={'pk': help_request.pk})
        data = {
            'title': 'Обновлённый заголовок',
            'description': 'Измененное описание',
            'topic': help_request.topic,
            'urgency': help_request.urgency
        }

        response = api_client.put(url, data, content_type='application/json')
        help_request.refresh_from_db()

        assert response.status_code == 403
        assert help_request.title != 'Измененное описание'

    def test_update_request_unauthenticated(self, api_client, help_request):

        url = reverse('request-detail', kwargs={'pk': help_request.pk})
        data = {
            'title': 'Обновлённый заголовок',
            'description': 'Измененное описание',
            'topic': help_request.topic,
            'urgency': help_request.urgency
        }

        response = api_client.put(url, data, content_type='application/json')
        help_request.refresh_from_db()

        assert response.status_code == 401


    def test_delete_request_author_success(self, api_client, help_request):
        api_client.force_authenticate(help_request.author)
        url = reverse('request-detail', kwargs={'pk': help_request.pk})

        response = api_client.delete(url)

        assert response.status_code == 204
        # assert not help_request.__class__.objects.filter(pk=help_request.pk).exists()

    def test_delete_request_authenticated_not_author(self, api_client, help_request, django_user_model):
        not_author = django_user_model.objects.create_user(email='wrong@wrong.com', password='12345')
        api_client.force_authenticate(not_author)
        url = reverse('request-detail', kwargs={'pk': help_request.pk})

        response = api_client.delete(url)

        assert response.status_code == 403
        # assert help_request.__class__.objects.filter(pk=help_request.pk).exists()
