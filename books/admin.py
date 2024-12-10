from django.contrib import admin

from books.models import Books, UserBookRelation

# Register your models here.
admin.site.register(Books)
admin.site.register(UserBookRelation)