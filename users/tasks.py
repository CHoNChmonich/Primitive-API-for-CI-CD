from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

from app import secrets

@shared_task
def send_weekly_email():
    # Здесь логика для отправки email всем пользователям
    users = User.objects.filter(is_active=True)
    for user in users:
        send_mail(
            'Не забывайте читать книги!',
            'Это напоминание, чтобы вы не забывали заходить на сайт и читать книги.',
            secrets.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
