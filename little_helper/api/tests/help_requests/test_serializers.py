import pytest

from help_requests.models import *
from help_requests.serializers import *
from tests.factories import UserFactory


@pytest.mark.django_db
class TestHelpRequestSerializer:

    def test_title_max_length(self):
        title_max_len = HelpRequest._meta.get_field("title").max_length
        request_data = {
            "title": "T" * (title_max_len + 1),
            "topic": "chat",
            "description": "Описание",
            "urgency": 1,
        }

        serializer_data = HelpRequestSerializer(data=request_data)

        assert not serializer_data.is_valid()
        assert "title" in serializer_data.errors

    def test_topic_max_length(self):
        topic_max_len = HelpRequest._meta.get_field("topic").max_length
        request_data = {
            "title": "Title",
            "topic": "T" * (topic_max_len + 1),
            "description": "Описание",
            "urgency": 1,
        }

        serializer_data = HelpRequestSerializer(data=request_data)

        assert not serializer_data.is_valid()
        assert "topic" in serializer_data.errors

    def test_valid_data_serialization(self):
        user = UserFactory()
        request_data = {
            "title": "Тест",
            "topic": "чат",
            "description": "Описание",
            "urgency": 2,
        }

        serializer_data = HelpRequestSerializer(data=request_data)

        assert serializer_data.is_valid()

        instance = serializer_data.save(author=user)

        assert instance.title == request_data["title"]
        assert instance.author == user
        assert instance.status == HelpRequest.Status.OPEN

    def test_missing_required_fields(self):
        request_data = {}

        serializer_data = HelpRequestSerializer(data=request_data)

        assert not serializer_data.is_valid()
        assert "title" in serializer_data.errors
        assert "topic" in serializer_data.errors
        assert "description" in serializer_data.errors

    def test_read_only_fields_ignored(self):
        user = UserFactory()
        request_data = {
            "title": "Тест",
            "topic": "Чат",
            "description": "Описание",
            "urgency": 1,
            "author": 999,
            "status": 5,
        }

        serializer_data = HelpRequestSerializer(data=request_data)

        assert serializer_data.is_valid(), serializer_data.errors

        instance = serializer_data.save(author=user)

        assert instance.author == user
        assert instance.status != 5
