from django.urls import path
from .views import UserRegistrationView, UserLoginView, LogoutAPIView, csrf_token_view, ActivateUserView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='email-verify'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', LogoutAPIView.as_view(), name='user-logout'),
    path('csrf/', csrf_token_view, name='token'),
]
