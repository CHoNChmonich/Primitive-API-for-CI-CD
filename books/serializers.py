from itertools import count

from rest_framework import serializers

from books.models import Books, LANGUAGE_CHOICES, UserBookRelation


class BooksSerializer(serializers.ModelSerializer):
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='ru')
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Books
        fields = ['id','name', 'description', 'price', 'author', 'language', 'annotated_likes', 'rating']


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']

