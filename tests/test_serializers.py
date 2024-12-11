from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from books.models import Books, UserBookRelation
from books.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')
        """Создаем тестовые данные для каждого теста"""
        self.book1 = Books.objects.create(
            name='Cool book',
            author='cool author',
            price='148',
            description='Nice',
            owner=self.user1,

        )
        self.book2 = Books.objects.create(
            name='Bad book',
            author='Karl Marx',
            price='0',
            description='For dumbass',
            owner=self.user1
        )

    def test_ok(self):
        serializer_data = BooksSerializer(
            Books.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))),
            many=True).data
        print(serializer_data)
        self.assertEqual(serializer_data, [
            {'id': 1, 'name': 'Cool book', 'description': 'Nice', 'price': '148.00', 'author': 'cool author',
             'language': 'ru', 'annotated_likes': 0, 'rating': None,
             'owner_name': 'test_user', 'readers': []},
            {'id': 2, 'name': 'Bad book', 'description': 'For dumbass', 'price': '0.00', 'author': 'Karl Marx',
             'language': 'ru', 'annotated_likes': 0, 'rating': None, 'owner_name': 'test_user', 'readers': []}]
                         )
