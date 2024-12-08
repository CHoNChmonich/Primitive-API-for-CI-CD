from rest_framework import serializers

from books.models import Books, LANGUAGE_CHOICES


class BooksSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    author = serializers.CharField(max_length=255)
    price = serializers.DecimalField(decimal_places=2, max_digits=7)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='ru')

    def create(self, validated_data):
        return Books.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.price = validated_data.get('price', instance.price)
        instance.language = validated_data.get('language', instance.language)
        instance.save()
        return instance
