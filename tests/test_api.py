from django.urls import reverse
from django.db import connection
from django.db.models import Count, Case, When, Avg
from django.test.utils import CaptureQueriesContext
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, \
    HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase
from rest_framework.utils import json

from books.models import Books, UserBookRelation
from books.serializers import BooksSerializer
from users.models import User


class BooksListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', is_staff=True)

        """Создаем тестовые данные для каждого теста"""
        self.book1 = Books.objects.create(
            name='Karl Marx ',
            author='on sam',
            price='1488',
            description='Nice'
        )
        self.book2 = Books.objects.create(
            name='Bad book',
            author='Karl Marx',
            price='2000',
            description='For dumbass'
        )
        self.url = reverse('books:books_list')

    def test_get(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(self.url)
            self.assertEqual(2, len(queries))
        serializer_data = BooksSerializer(
            Books.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))),
            many=True).data
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_with_search(self):
        response = self.client.get(self.url, query_params={'search': 'Karl Marx'})
        self.assertEqual(response.data, BooksSerializer(
            Books.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))),
            many=True).data
                         )

    def test_get_with_filter(self):
        response = self.client.get(self.url, query_params={'price': '1488'})
        serializer_data = BooksSerializer(Books.objects.filter(id=self.book1.id).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))))[0]).data
        self.assertEqual(response.data, [serializer_data])

    def test_get_with_ordering(self):
        response = self.client.get(self.url, query_params={'ordering': 'price'})
        self.assertEqual(response.data, BooksSerializer(
            Books.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))),
            many=True).data)

    def test_post_admin(self):
        new_book_data = {
            'name': 'New book',
            'author': 'New Author',
            'description': 'A new book description',
            'price': '3000.00',  # Убедитесь, что цена соответствует формату Decimal
            'language': 'ru'  # Или любое другое значение из ваших choices
        }
        # Отправляем post-запрос с данным на сервер
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=new_book_data, format='json')
        # Проверяем создался ли новый объект
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Books.objects.count(), 3)
        self.assertEqual(Books.objects.last().name, new_book_data['name'])
        self.assertEqual(Books.objects.last().author, new_book_data['author'])
        self.assertEqual(str(Books.objects.last().price), new_book_data['price'])
        self.assertEqual(Books.objects.last().description, new_book_data['description'])
        self.assertEqual(Books.objects.last().owner, self.user)

    def test_post_authenticated_user(self):
        new_book_data = {
            'name': 'New book',
            'author': 'New Author',
            'description': 'A new book description',
            'price': '3000.00',  # Убедитесь, что цена соответствует формату Decimal
            'language': 'ru'  # Или любое другое значение из ваших choices
        }
        authenticated_user = User.objects.create(username='authenticated_user')
        # Отправляем post-запрос с данным на сервер
        self.client.force_login(authenticated_user)
        response = self.client.post(self.url, data=new_book_data, format='json')
        # Проверяем создался ли новый объект
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Books.objects.count(), 3)
        self.assertEqual(Books.objects.last().name, new_book_data['name'])
        self.assertEqual(Books.objects.last().author, new_book_data['author'])
        self.assertEqual(str(Books.objects.last().price), new_book_data['price'])
        self.assertEqual(Books.objects.last().description, new_book_data['description'])
        self.assertEqual(Books.objects.last().owner, authenticated_user)

    def test_post_not_allowed(self):
        new_book_data = {
            'name': 'New book',
            'author': 'New Author',
            'description': 'A new book description',
            'price': '3000.00',  # Убедитесь, что цена соответствует формату Decimal
            'language': 'ru'  # Или любое другое значение из ваших choices
        }
        # Отправляем post-запрос с данным на сервер
        response = self.client.post(self.url, data=new_book_data, format='json')
        # Проверяем создался ли новый объект
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(Books.objects.count(), 2)


class BookDetailUpdateDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', is_staff=True)
        self.owner_user = User.objects.create(username='owner_username')
        """Создаем тестовые данные для каждого теста"""
        self.book1 = Books.objects.create(
            name='Cool book',
            author='Nikolay',
            price='148',
            description='Nice',
            owner=self.owner_user
        )
        self.book2 = Books.objects.create(
            name='Bad book',
            author='Nikita',
            price='0',
            description='For dumbass',
            owner=self.owner_user
        )
        self.url = reverse('books:books_detail', kwargs={'pk': self.book1.id})

    def test_get(self):
        # Тестируем получение существующей книги
        response = self.client.get(self.url)
        serializer_data = BooksSerializer(self.book1).data
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_get_not_found(self):
        # Тестируем получение несуществующей книги
        not_found_url = reverse('books:books_detail', kwargs={'pk': 999})
        response_not_found = self.client.get(not_found_url)
        self.assertEqual(response_not_found.status_code, HTTP_404_NOT_FOUND)

    def test_put_admin(self):
        self.client.force_login(self.user)
        # Проверяем на работоспособность PUT-запрос
        new_book_data = {
            'name': 'New book',
            'author': 'New Author',
            'description': 'A new book description',
            'price': '19.99',  # Убедитесь, что цена соответствует формату Decimal
            'language': 'ru'  # Или любое другое значение из ваших choices
        }
        # Проверяем статус код
        response = self.client.put(self.url, data=new_book_data, format='json')  # Убедитесь, что формат JSON
        self.assertEqual(response.status_code, HTTP_200_OK)
        # Проверяем изменились ли данные из бд
        self.book1.refresh_from_db()  # Нужно чтобы актуализировать данные о записи
        self.assertEqual(self.book1.name, new_book_data['name'])
        self.assertEqual(self.book1.author, new_book_data['author'])
        self.assertEqual(self.book1.description, new_book_data['description'])
        self.assertEqual(str(self.book1.price), new_book_data['price'])
        self.assertEqual(self.book1.language, new_book_data['language'])

    def test_put_owner(self):
        self.client.force_login(self.owner_user)
        # Проверяем на работоспособность PUT-запрос
        new_book_data = {
            'name': 'New book',
            'author': 'New Author',
            'description': 'A new book description',
            'price': '19.99',  # Убедитесь, что цена соответствует формату Decimal
            'language': 'ru'  # Или любое другое значение из ваших choices
        }
        # Проверяем статус код
        response = self.client.put(self.url, data=new_book_data, format='json')  # Убедитесь, что формат JSON
        self.assertEqual(response.status_code, HTTP_200_OK)
        # Проверяем изменились ли данные из бд
        self.book1.refresh_from_db()  # Нужно чтобы актуализировать данные о записи
        self.assertEqual(self.book1.name, new_book_data['name'])
        self.assertEqual(self.book1.author, new_book_data['author'])
        self.assertEqual(self.book1.description, new_book_data['description'])
        self.assertEqual(str(self.book1.price), new_book_data['price'])
        self.assertEqual(self.book1.language, new_book_data['language'])

    def test_put_not_found(self):
        self.client.force_login(self.user)
        # Проверяем на работоспособность PUT-запрос
        new_book_data = {
            'name': 'New book',
            'author': 'New Author',
            'description': 'A new book description',
            'price': '19.99',  # Убедитесь, что цена соответствует формату Decimal
            'language': 'ru'  # Или любое другое значение из ваших choices
        }
        not_found_url = reverse('books:books_detail', kwargs={'pk': 999})
        response_not_found = self.client.put(not_found_url, data=new_book_data)
        self.assertEqual(response_not_found.status_code, HTTP_404_NOT_FOUND)

    def test_put_not_allowed_anonymous(self):
        new_book_data = {
            'name': 'New book',
            'author': 'New Author',
            'description': 'A new book description',
            'price': '19.99',  # Убедитесь, что цена соответствует формату Decimal
            'language': 'ru'  # Или любое другое значение из ваших choices
        }
        response_not_allowed = self.client.put(self.url, data=new_book_data, format='json')
        self.assertEqual(response_not_allowed.status_code, HTTP_403_FORBIDDEN)

    def test_put_not_allowed_not_owner(self):
        not_owner = User.objects.create(username='not_owner')
        new_book_data = {
            'name': 'New book',
            'author': 'New Author',
            'description': 'A new book description',
            'price': '19.99',  # Убедитесь, что цена соответствует формату Decimal
            'language': 'ru'  # Или любое другое значение из ваших choices
        }
        self.client.force_login(not_owner)
        response_not_allowed = self.client.put(self.url, data=new_book_data, format='json')
        self.assertEqual(response_not_allowed.status_code, HTTP_403_FORBIDDEN)

    def test_delete_admin(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_delete_owner(self):
        self.client.force_login(self.owner_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_delete_not_found(self):
        self.client.force_login(self.user)
        # Проверяем на работоспособность PUT-запрос
        not_found_url = reverse('books:books_detail', kwargs={'pk': 999})
        response_not_found = self.client.delete(not_found_url)
        self.assertEqual(response_not_found.status_code, HTTP_404_NOT_FOUND)

    def test_delete_not_allowed_anonymous(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_delete_not_allowed_not_owner(self):
        not_owner = User.objects.create(username='not_owner')
        self.client.force_login(not_owner)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user_admin = User.objects.create(username='admin', is_staff=True)
        """Создаем тестовые данные для каждого теста"""
        self.book1 = Books.objects.create(
            name='Cool book',
            author='Adolf Hitler',
            price='1488',
            description='Nice',
            owner=self.user_admin
        )
        self.book2 = Books.objects.create(
            name='Bad book',
            author='Karl Marx',
            price='0',
            description='For dumbass',
            owner=self.user_admin
        )

    def test_like(self):
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(relation.like)

    def test_bookmarks(self):
        data = {
            'in_bookmarks': True,
        }
        json_data = json.dumps(data)
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        data = {
            'rate': 5,
        }
        json_data = json.dumps(data)
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertEqual(response.status_code, HTTP_200_OK, response.data)
        self.assertEqual(relation.rate, 5, response.data)

    def test_rate_wrong(self):
        data = {
            'rate': 7,
        }
        json_data = json.dumps(data)
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        relation = UserBookRelation.objects.get(user=self.user1, book=self.book1)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST, response.data)
