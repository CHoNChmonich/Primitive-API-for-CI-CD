from django.contrib.auth.models import User
from rest_framework import serializers

from books.models import Books, LANGUAGE_CHOICES, UserBookRelation


class BookReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['first_name', 'last_name']



class BooksSerializer(serializers.ModelSerializer):
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='ru')
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner.username', default='Have not owner', read_only=True)
    readers  = BookReaderSerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Books
        fields = ['id','name', 'description', 'price', 'author', 'language', 'annotated_likes', 'rating', 'owner_name', 'readers']


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']

