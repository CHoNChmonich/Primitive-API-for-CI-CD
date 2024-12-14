from django.db import models
from users.models import User

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
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='readed_books')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    def __str__(self):
        return f'{self.name} за авторством {self.author} | {self.id}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_book_relation')
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=1)

    def __str__(self):
        return f'{self.user.username} имеет отношение к книге {self.book.name} | Лайкнул: {self.like} | В закладках: {self.in_bookmarks} | Рейтинг: {self.rate}'

    def save(self, *args, **kwargs):
        old_rate = self.rate
        is_created = not self.pk
        super().save(*args, **kwargs)
        new_rate = self.rate
        from books.logic import set_rating
        if old_rate != new_rate or is_created:
            set_rating(self.book)