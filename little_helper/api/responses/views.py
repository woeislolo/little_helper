from rest_framework import generics, permissions

from .permissions import ResponsePermission
from .models import *
from .serializers import *
from help_requests.models import *


class ResponseListCreateView(generics.ListCreateAPIView):
    """
    GET: возвращает список откликов на запрос (по id)
    POST: создает отклик на запрос
    """
    serializer_class = ResponseSerializer
    permission_classes = [ResponsePermission,]

    def get_help_request(self):
        return HelpRequest.objects.get(pk=self.kwargs["request_id"])

    def get_queryset(self):
        return Response.objects.filter(help_request=self.get_help_request())

    def perform_create(self, serializer):
        serializer.save(
            responder=self.request.user,
            help_request=self.get_help_request()
        )


class ResponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: получает отклик (по id)
    PUT/PATCH: изменяет отклик
    DELETE: удаляет отклик
    """
    serializer_class = ResponseSerializer
    permission_classes = [ResponsePermission,]

    def get_queryset(self):
        request_id = self.kwargs["request_id"]
        return Response.objects.filter(help_request_id=request_id)
