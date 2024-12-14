from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

def send_verification_email(user, request):
    """Отправка email с ссылкой для активации аккаунта"""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = request.build_absolute_uri(
        reverse('users:email-verify', kwargs={'uidb64': uid, 'token': token})
    )
    subject = 'Подтверждение регистрации'
    message = f'Здравствуйте, {user.username}!\n\nПодтвердите вашу регистрацию по ссылке:\n{activation_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [user.email])
