from rest_framework import serializers

from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    responder = serializers.ReadOnlyField(source="responder.email")

    class Meta:
        model = Response
        fields = ["id", "help_request", "responder", "message", "status", "created_at"]
        read_only_fields = ["id", "responder", "created_at"]
