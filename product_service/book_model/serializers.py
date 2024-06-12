from cloudinary.uploader import upload
from rest_framework import serializers
from .models import Book, Category, Author, Publisher


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    author = AuthorSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

