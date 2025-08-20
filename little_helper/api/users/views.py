from django.contrib.auth import get_user_model, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *


CustomUser = get_user_model()


class RegisterView(generics.CreateAPIView):
    """ Регистрация """

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """ Логин """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response(data={'detail': 'Invalid credentials'}, 
                        status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(ReadOnlyModelViewSet):
    """ Возвращает одного или всех юзеров """

    queryset = CustomUser.objects.all() 
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]


class MeView(APIView):
    """ Возвращает инфо по авторизованному юзеру """
    
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
