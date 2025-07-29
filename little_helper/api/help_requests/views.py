from rest_framework import generics, permissions, mixins

from .models import *
from .serializers import *
from .permissions import *


class HelpRequestListCreateView(generics.ListCreateAPIView):
    """ Возвращает список всех заявок либо создает заявку """

    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated,]

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
