from django.db import models
from django.conf import settings


class HelpRequest(models.Model):

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In progress'
        CLOSED = 'closed', 'Closed'

    class Urgency(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'


    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='help_requests'
    )
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=100)
    description = models.TextField()
    urgency = models.IntegerField(
        choices=Urgency.choices,
        default=Urgency.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} ({self.status})"
