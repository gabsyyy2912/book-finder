# Generated by Django 5.1.2 on 2025-03-01 06:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(max_length=100),
        ),
        migrations.RemoveField(
            model_name='author',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='review',
            name='content',
        ),
        migrations.AddField(
            model_name='author',
            name='biography',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.TextField(default='No comment available'),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer_name',
            field=models.CharField(default='Anonymous', max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
    ]
