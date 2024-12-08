from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from books.models import Books
from books.serializers import BooksSerializer


class BooksListTestCase(APITestCase):
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
        self.url = reverse('books:books_list')

    def test_get(self):
        response = self.client.get(self.url)
        serializer_data = BooksSerializer([self.book1, self.book2], many=True).data
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)
