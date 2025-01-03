from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from books.permissions import IsAuthenticatedOrAdminOrReadOnly, IsOwnerOrAdminOrReadOnly
from books.models import Books, UserBookRelation
from books.serializers import BooksSerializer, UserBookRelationSerializer


def auth(request):
    return render(request, 'books/oauth.html')


class BooksListCreateAPIView(ListCreateAPIView):
    queryset = Books.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
                                            ).select_related('owner').prefetch_related('readers')
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticatedOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price', 'author']
    search_fields = ['name', 'description', 'author']
    ordering_fields = ['price', 'author']
    ordering = ['price']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class BooksDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = BooksSerializer


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    queryset = UserBookRelation.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        return obj


class ProtectedAPIView(ListAPIView):
    serializer_class = BooksSerializer
    queryset = Books.objects.all()
    permission_classes = [IsAuthenticated]