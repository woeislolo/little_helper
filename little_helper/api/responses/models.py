from django.db import models
from django.conf import settings

from help_requests.models import *


class Response(models.Model):

    class Status(models.IntegerChoices):
        PENDING = 1, 'Pending'
        ACCEPTED = 2, 'Accepted'
        REJECTED = 3, 'Rejected'

    help_request = models.ForeignKey(
        HelpRequest,
        on_delete=models.CASCADE,
        related_name='responses'
        )
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responses'
        )
    message = models.TextField(blank=True, null=True)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PENDING)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отклик пользователя {self.responder.email} на HelpRequest {self.help_request}"
    