# Generated by Django 4.0.1 on 2024-04-28 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_model', '0003_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
