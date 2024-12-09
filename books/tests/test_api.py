from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from books.models import Books
from books.serializers import BooksSerializer


class BooksListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', is_staff=True)

        """Создаем тестовые данные для каждого теста"""
        self.book1 = Books.objects.create(
            name='Karl Marx Huesos',
            author='Adolf Hitler',
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
        response = self.client.get(self.url)
        serializer_data = BooksSerializer([self.book1, self.book2], many=True).data
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_with_search(self):
        response = self.client.get(self.url, query_params={'search': 'Karl Marx'})
        self.assertEqual(response.data, BooksSerializer([self.book1, self.book2], many=True).data)

    def test_get_with_filter(self):
        response = self.client.get(self.url, query_params={'price': '1488'})
        serializer_data = BooksSerializer(self.book1).data
        self.assertEqual(response.data, [serializer_data])

    def test_get_with_ordering(self):
        response = self.client.get(self.url, query_params={'ordering': 'price'})
        self.assertEqual(response.data, BooksSerializer([self.book1, self.book2], many=True).data)

    def test_post(self):
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
        # Проверяем количество объектов в бд


class BookDetailUpdateDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', is_staff=True)
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

    def test_put(self):
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

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
