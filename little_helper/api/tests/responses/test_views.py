from django.urls import reverse

import pytest

from users.models import *
from help_requests.models import *
from responses.models import *
from responses.serializers import *
from help_requests.urls import *


@pytest.mark.django_db
class TestResponseListCreateView:

    def setup_method(self):
        self.request_author = CustomUser.objects.create_user(
            email='test@test.com', 
            password='pass1234'
            )
        self.response_author = CustomUser.objects.create_user(
            email='test2@test.com', 
            password='pass1234'
            )

        self.helprequest=HelpRequest.objects.create(
            author=self.request_author,
            title='Тестовый запрос',
            description='Тестовое описание',
            topic='chat',
            )
        self.response = Response.objects.create(
            help_request=self.helprequest, 
            responder=self.response_author, 
            message='bla bla bla',
            )


    def test_get_responses_unauthenticated(self, api_client):
        url = reverse('response-list-create', kwargs={'request_id': self.helprequest.id})

        response = api_client.get(url)

        assert response.status_code == 401

    def test_get_responses_authenticated(self, auth_client):
        url = reverse('response-list-create', kwargs={'request_id': self.helprequest.id})

        response = auth_client.get(url)

        assert response.status_code == 403

    def test_get_responses_by_request_author(self, api_client):
        url = reverse('response-list-create', kwargs={'request_id': self.helprequest.id})
        api_client.force_authenticate(self.request_author)

        result = api_client.get(url)

        assert result.status_code == 200
        assert result.data[0]['help_request'] == self.helprequest.id
        assert result.data[0]['responder'] == self.response_author.email
        assert result.data[0]['message'] == self.response.message


    def test_create_response_by_unauthenticated(self, api_client):
        url = reverse('response-list-create', kwargs={'request_id': self.helprequest.id})

        data = {
            'help_request': self.helprequest.id, 
            'message': 'bla bla bla',
        }

        result = api_client.post(url, data=data, format='json')

        assert result.status_code == 401

    def test_create_response_by_authenticated(self, auth_client):
        url = reverse('response-list-create', kwargs={'request_id': self.helprequest.id})

        data = {
            'help_request': self.helprequest.id, 
            'message': 'bla bla bla',
        }

        result = auth_client.post(url, data=data, format='json')

        assert result.status_code == 201
        assert result.data['help_request'] == self.helprequest.id
        assert result.data['message'] == self.response.message

    def test_create_response_without_message_by_authenticated(self, auth_client):
        url = reverse('response-list-create', kwargs={'request_id': self.helprequest.id})

        data = {
            'help_request': self.helprequest.id,
        }

        result = auth_client.post(url, data=data, format='json')

        assert result.status_code == 201
        assert result.data['help_request'] == self.helprequest.id
        assert result.data['message'] == None

    def test_create_response_by_request_author(self, api_client):
        url = reverse('response-list-create', kwargs={'request_id': self.helprequest.id})
        api_client.force_authenticate(self.helprequest.author)
        data = {
            'help_request': self.helprequest.id, 
            'message': 'bla bla bla',
        }

        result = api_client.post(url, data=data, format='json')

        assert result.status_code == 403


@pytest.mark.django_db
class TestResponseDetailView:

    def setup_method(self):
        self.request_author = CustomUser.objects.create_user(
            email='test@test.com', 
            password='pass1234'
            )
        self.response_author = CustomUser.objects.create_user(
            email='test2@test.com', 
            password='pass1234'
            )

        self.helprequest=HelpRequest.objects.create(
            author=self.request_author,
            title='Тестовый запрос',
            description='Тестовое описание',
            topic='chat',
            )
        self.response = Response.objects.create(
            help_request=self.helprequest, 
            responder=self.response_author, 
            message='bla bla bla',
            )


    def test_get_response_by_requests_author(self, api_client): 
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        api_client.force_authenticate(self.helprequest.author)
        
        result = api_client.get(url)

        assert result.status_code == 200
        assert result.data['help_request'] == self.helprequest.id
        assert result.data['responder'] == self.response_author.email
           
    def test_get_response_by_responses_author(self, api_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        api_client.force_authenticate(self.response.responder)

        result = api_client.get(url)

        assert result.status_code == 200
        assert result.data['help_request'] == self.helprequest.id
        assert result.data['responder'] == self.response_author.email

    def test_get_response_by_other_auth_user(self, auth_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        
        result = auth_client.get(url)

        assert result.status_code == 403

    def test_get_response_by_unauth_user(self, api_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        
        result = api_client.get(url)

        assert result.status_code == 401


    def test_patch_response_by_requests_author(self, api_client): 
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        api_client.force_authenticate(self.helprequest.author)
        data = {
            'message': 'измененное сообщение'
        }
        
        result = api_client.patch(url, data=data, format='json')

        assert result.status_code == 403
        
    def test_patch_response_by_responses_author(self, api_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        api_client.force_authenticate(self.response.responder)
        data = {
            'message': 'измененное сообщение'
        }

        result = api_client.patch(url, data=data, format='json')

        assert result.status_code == 200
        assert result.data['help_request'] == self.helprequest.id
        assert result.data['message'] == 'измененное сообщение'

    def test_patch_response_by_other_auth_user(self, auth_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        data = {
            'message': 'измененное сообщение'
        }

        result = auth_client.patch(url, data=data, format='json')

        assert result.status_code == 403

    def test_patch_response_by_unauth_user(self, api_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        data = {
            'message': 'измененное сообщение'
        }

        result = api_client.patch(url, data=data, format='json')

        assert result.status_code == 401


    def test_delete_response_by_requests_author(self, api_client): 
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        api_client.force_authenticate(self.helprequest.author)
        
        result = api_client.delete(url)

        assert result.status_code == 403
        
    def test_delete_response_by_responses_author(self, api_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        api_client.force_authenticate(self.response.responder)

        result = api_client.delete(url)

        assert result.status_code == 204

    def test_delete_response_by_other_auth_user(self, auth_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})
        
        result = auth_client.delete(url)

        assert result.status_code == 403

    def test_delete_response_by_unauth_user(self, api_client):
        url = reverse('response-detail', kwargs={'request_id': self.helprequest.id,
                                                 'pk': self.response.pk})

        result = api_client.delete(url)

        assert result.status_code == 401
