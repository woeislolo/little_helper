from rest_framework import generics, permissions, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .permissions import *


class HelpRequestListCreateView(generics.ListCreateAPIView):
    """ Возвращает список всех заявок либо создает заявку """

    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['status', 'urgency', 'topic']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class HelpRequestRetrieveView(generics.RetrieveAPIView):
    """ Возвращает заявку по id """

    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated,]


class HelpRequestUpdateDestroyView(mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   generics.GenericAPIView):
    """ Изменяет или удаляет заявку по id (только автор заявки) """

    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdminOrReadOnly]


class MyHelpRequestsListView(generics.ListAPIView):
    """ Возвращает список заявок юзера """

    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return HelpRequest.objects.filter(author=self.request.user)


class CloseHelpRequestView(APIView):
    """ Меняет статус заявки на closed """

    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdminOrReadOnly]

    def post(self, request, pk):
        try:
            help_request = HelpRequest.objects.get(pk=pk)
        except HelpRequest.DoesNotExist:
            return Response({'detail': 'Not found'}, 
                            status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, help_request)

        help_request.status = HelpRequest.Status.CLOSED
        help_request.save()
        
        return Response(HelpRequestSerializer(help_request).data)
