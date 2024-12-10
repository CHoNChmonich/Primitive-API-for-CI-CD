from django.test import TestCase
from django.contrib.auth.models import User

from books.models import Books
from books.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        """Создаем тестовые данные для каждого теста"""
        self.book1 = Books.objects.create(
            name='Cool book',
            author='Adolf Hitler',
            price='1488',
            description='Nice',
            owner=self.user
        )
        self.book2 = Books.objects.create(
            name='Bad book',
            author='Karl Marx',
            price='0',
            description='For dumbass',
            owner=self.user
        )

    def test_ok(self):
        serializer_data = BooksSerializer([self.book1, self.book2], many=True).data
        self.assertEqual(serializer_data, [
            {'id': 1, 'language': 'ru', 'owner_id': 1, 'name': 'Cool book', 'description': 'Nice',
             'author': 'Adolf Hitler', 'price': '1488.00', 'owner': 1},
            {'id': 2, 'language': 'ru', 'owner_id': 1, 'name': 'Bad book', 'description': 'For dumbass',
             'author': 'Karl Marx', 'price': '0.00', 'owner': 1}])
