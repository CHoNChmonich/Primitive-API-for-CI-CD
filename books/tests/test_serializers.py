from django.test import TestCase

from books.models import Books
from books.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def setUp(self):
        """Создаем тестовые данные для каждого теста"""
        self.book1 = Books.objects.create(
            name='Cool book',
            author='Adolf Hitler',
            price='1488',
            description='Nice'
        )
        self.book2 = Books.objects.create(
            name='Bad book',
            author='Karl Marx',
            price='0',
            description='For dumbass'
        )

    def test_ok(self):
        serializer_data = BooksSerializer([self.book1, self.book2], many=True).data
        self.assertEqual(serializer_data, [
            {'name': 'Cool book', 'description': 'Nice', 'author': 'Adolf Hitler', 'price': '1488.00',
             'language': 'ru'},
            {'name': 'Bad book', 'description': 'For dumbass', 'author': 'Karl Marx', 'price': '0.00',
             'language': 'ru'}])
