from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from books.permissions import IsAdminOrReadOnly
from books.models import Books
from books.serializers import BooksSerializer

def auth(request):
    return render(request, 'books/oauth.html')

class BooksListCreateAPIView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price', 'author']
    search_fields = ['name', 'description', 'author']
    ordering_fields = ['price', 'author']
    ordering = ['price']


class BooksDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
