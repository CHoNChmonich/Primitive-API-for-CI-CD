from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from books.views import *

app_name = 'books'

urlpatterns = [
    path('', BooksListCreateAPIView.as_view(), name='books_list'),
    path('<int:pk>/', BooksDetailUpdateDeleteAPIView.as_view(), name='books_detail')
]
urlpatterns = format_suffix_patterns(urlpatterns)