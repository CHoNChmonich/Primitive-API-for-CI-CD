from rest_framework import serializers

from books.models import Books, LANGUAGE_CHOICES, UserBookRelation


class BooksSerializer(serializers.ModelSerializer):
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='ru')
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Books
        fields = '__all__'


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'in_bookmarks', 'rate']

