from django.db import models

LANGUAGE_CHOICES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'ru': 'Russian'
}


class Books(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='ru', max_length=100)
