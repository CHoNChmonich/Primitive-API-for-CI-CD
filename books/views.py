from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from books.models import Books
from books.serializers import BooksSerializer


class BooksListCreateAPIView(APIView):
    def get(self, request, format=None):
        books = Books.objects.all()
        serializer = BooksSerializer(instance=books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksDetailUpdateDeleteAPIView(APIView):
    def get_object(self, request, pk, format=None):

        return get_object_or_404(Books, id=pk)

    def get(self, request, pk, format=None):
        book = self.get_object(request, pk)
        serializer = BooksSerializer(instance=book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(request, pk)
        serializer = BooksSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(request, pk)
        book.delete()
        return Response(status=HTTP_204_NO_CONTENT)
