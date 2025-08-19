import pytest

from help_requests.models import *
from users.models import *
from tests.factories import UserFactory


@pytest.mark.django_db
class TestHelpRequest:

    def setup_method(self):
        self.user = UserFactory()

    def test_create_request_default_values(self, help_request):
        assert help_request.urgency == HelpRequest.Urgency.MEDIUM
        assert help_request.status == HelpRequest.Status.OPEN

    def test_create_request_custom_values(self):
        help_request = HelpRequest.objects.create(
            author=self.user,
            title="Need help",
            topic="IT",
            description="Something is not working",
            urgency=HelpRequest.Urgency.HIGH,
            status=HelpRequest.Status.IN_PROGRESS
        )

        assert help_request.urgency == HelpRequest.Urgency.HIGH
        assert help_request.status == HelpRequest.Status.IN_PROGRESS


    def test_update_status_and_urgency(self):
        help_request = HelpRequest.objects.create(
            author=self.user,
            title="Need help",
            topic="IT",
            description="Something is not working",
        )

        help_request.status = HelpRequest.Status.CLOSED
        help_request.urgency = HelpRequest.Urgency.LOW
        help_request.save()

        updated = HelpRequest.objects.get(pk=help_request.pk)
        assert updated.status == HelpRequest.Status.CLOSED
        assert updated.urgency == HelpRequest.Urgency.LOW


    def test_request_title_max_length(self, help_request):
        max_length = help_request._meta.get_field("title").max_length

        assert max_length == 255

    def test_request_topic_max_length(self, help_request):
        max_length = help_request._meta.get_field("topic").max_length

        assert max_length == 100

    def test_after_deleting_author_request_doesnt_exist(self):
        author = UserFactory()
        HelpRequest.objects.create(
            author=author,
            title='Тестовый запрос',
            description='Тестовое описание',
            topic='chat',
            )
        
        author.delete()
        help_request = len(HelpRequest.objects.all())

        assert help_request == 0

    def test_request_description_can_be_blank(self):
        author = UserFactory()
        help_request = HelpRequest.objects.create(
            author=author,
            title='Тестовый запрос 123',
            topic='chat',
            )
        
        assert help_request.title == 'Тестовый запрос 123'
