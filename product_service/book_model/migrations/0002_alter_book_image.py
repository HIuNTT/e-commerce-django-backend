# Generated by Django 4.0.1 on 2024-04-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_model', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.URLField(),
        ),
    ]
