from django.core.management import call_command

from rest_framework.test import APIClient

import pytest

from tests.factories import UserFactory
from help_requests.models import *


@pytest.fixture
def api_client():
    """Неавторизованный API клиент"""
    return APIClient()

@pytest.fixture
def auth_user(db):
    """Создаёт пользователя и возвращает его"""
    return UserFactory()

@pytest.fixture
def auth_client(auth_user):
    """Авторизованный API клиент"""
    client = APIClient()
    client.force_authenticate(user=auth_user)
    return client

@pytest.fixture
def help_request(db):
    """Help request"""
    author = UserFactory()

    return HelpRequest.objects.create(
        author=author,
        title='Тестовый запрос',
        description='Тестовое описание',
        topic='chat',
    )

# @pytest.fixture(scope="function", autouse=True)
# def load_test_data(db, django_db_blocker):
#     print("loading data....")
#     with django_db_blocker.unblock():
#         call_command("loaddata", "test.json", database="default")
