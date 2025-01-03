from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.contrib.auth import  authenticate
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegisterSerializer
from users.utils import send_verification_email
from users.models import User


class UserRegistrationView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # user.is_active = False
            # user.save()
            send_verification_email(user, request)
            return Response({'message': 'Вы успешно зарегистрированы. Проверьте почту для активации аккаунта.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_verified = True
            user.is_active = True
            user.save()
            return Response({'message': 'Ваш аккаунт успешно активирован!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Недействительная ссылка или пользователь не найден.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            return Response({'error': 'Введите логин и пароль'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Неверные данные, пользователь не найден'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh_token')  # С клиента нужно отправить refresh token
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавить его в чёрный список
        except Exception as e:
            return Response({'error': 'Неверный Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def csrf_token_view(request):
    token = get_token(request)
    return Response({'csrfToken': token}, status=status.HTTP_200_OK)

