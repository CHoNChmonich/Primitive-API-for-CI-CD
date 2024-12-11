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
            author='Adolf Hitler',
            price='1488',
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
        UserBookRelation.objects.create(user=self.user1, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=True, rate=5)

        UserBookRelation.objects.create(user=self.user1, book=self.book2, like=False, rate=3)
        UserBookRelation.objects.create(user=self.user2, book=self.book2, like=False)
        UserBookRelation.objects.create(user=self.user3, book=self.book2, like=True)

    def test_ok(self):
        serializer_data = BooksSerializer(
            Books.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg('userbookrelation__rate')),
            many=True).data
        print(serializer_data)
        self.assertEqual(serializer_data, [
            {'id': 1, 'name': 'Cool book', 'description': 'Nice', 'price': '1488.00', 'author': 'Adolf Hitler',
             'language': 'ru', 'annotated_likes': 3, 'rating': '5.00'},
            {'id': 2, 'name': 'Bad book', 'description': 'For dumbass', 'price': '0.00', 'author': 'Karl Marx',
             'language': 'ru', 'annotated_likes': 1, 'rating': '1.67'}]
                         )
