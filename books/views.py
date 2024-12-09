from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from books.models import Books
from books.serializers import BooksSerializer


class BooksListCreateAPIView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer



class BooksDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
