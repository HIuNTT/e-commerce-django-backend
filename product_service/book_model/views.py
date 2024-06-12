import re
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Book, Category, Author, Publisher
from .serializers import BookSerializer


# Create your views here.


# Get list books, search book by keyword
class BookViewSet(viewsets.ViewSet,
                  generics.ListAPIView):

    queryset = Book.objects.filter(is_active__in=[True])
    serializer_class = BookSerializer

    # Tìm book theo keyword
    @action(detail=False, methods=['get'], url_path='search/(?P<keyword>[^/.]+)')
    def search(self, request, keyword=''):
        words = keyword.split()
        # Lấy ra danh sách khớp với từ đầu tiên của keyword
        books = Book.objects.filter(Q(name__icontains=words[0]) | Q(slug__icontains=words[0]) | Q(description__icontains=words[0])).order_by('name')
        # Tiếp tục lặp các từ còn lại
        for word in words:
            books = books.filter(Q(name__icontains=word) | Q(slug__icontains=word) | Q(description__icontains=word))
        if books.exists():
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# Get a boọk by slug or id
class BookSlugOrIdViewSet(APIView):
    def get(self, request, str):
        try:
            if re.search("\w-", str):
                slug = str
                book = Book.objects.get(slug=slug, is_active__in=[True])
            else:
                id = str
                book = Book.objects.get(id=id, is_active__in=[True])
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'message': 'Not found with provided slug'}, status=status.HTTP_404_NOT_FOUND)


# Get list books by category id
class ListBookOfCategoryViewSet(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        return category.books.filter(is_active__in=[True]).order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'message': 'No books found for this category'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = BookSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# Get list books by author id
class ListBookOfAuthorViewSet(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        author_id = self.kwargs['author_id']
        author = get_object_or_404(Author, id=author_id)
        return author.books.filter(is_active__in=[True]).order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'message': 'No books found for this author'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = BookSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ListBookOfPublisherViewSet(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        publisher_id = self.kwargs['publisher_id']
        publisher = get_object_or_404(Publisher, id=publisher_id)
        return publisher.books.filter(is_active__in=[True]).order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'message': 'No books found for this publisher'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = BookSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)