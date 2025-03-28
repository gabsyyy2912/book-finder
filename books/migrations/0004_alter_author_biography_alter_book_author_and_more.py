# Generated by Django 5.1.2 on 2025-03-01 06:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='biography',
            field=models.TextField(default='This author has not provided a biography.'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer_name',
            field=models.CharField(max_length=255),
        ),
    ]
