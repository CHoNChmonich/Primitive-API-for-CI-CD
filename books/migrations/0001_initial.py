# Generated by Django 5.1.4 on 2024-12-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('author', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('language', models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('ru', 'Russian')], default='ru', max_length=100)),
                ('rating', models.DecimalField(decimal_places=2, default=None, max_digits=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserBookRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('in_bookmarks', models.BooleanField(default=False)),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
            ],
        ),
    ]
