from rest_framework import serializers

from .models import *


class HelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = ['id', 'author', 'title', 'topic', 'description', 'urgency', 'status', 'created_at']
        read_only_fields = ['author', 'status', 'created_at']
