from django.db import models
from django.contrib.auth.models import User
from pycparser.ply.yacc import default_lr

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
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='books')

    def __str__(self):
        return f'{self.name} за авторством {self.author} | {self.id}'



class UserBookRelation(models.Model):
    RATE_CHOICES = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_book')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='related_user')
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=1)