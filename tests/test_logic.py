from django.test import TestCase
from django.contrib.auth.models import User

from books.logic import set_rating
from books.models import Books, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user')
        """Создаем тестовые данные для каждого теста"""
        self.book = Books.objects.create(
            name='Cool book',
            author='Adolf Hitler',
            price='1488',
            description='Nice',
            owner=self.user1,

        )
        UserBookRelation.objects.create(book=self.book, user=self.user1, rate=5)

    def test_ok(self):
        set_rating(self.book)
        self.assertEqual(self.book.rating, 5.0)