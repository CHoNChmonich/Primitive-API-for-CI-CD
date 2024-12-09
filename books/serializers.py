from rest_framework import serializers

from books.models import Books, LANGUAGE_CHOICES

class BooksSerializer(serializers.ModelSerializer):
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='ru')
    class Meta:
        model = Books
        fields = ['name', 'description', 'author', 'price', 'language']
