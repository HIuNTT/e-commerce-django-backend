import re
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Clothes, Producer, Style
from .serializers import ClothesSerializer


# Create your views here.


# Get list clothes, search clothes by keyword
class ClothesViewSet(viewsets.ViewSet,
                  generics.ListAPIView):

    queryset = Clothes.objects.filter(is_active__in=[True])
    serializer_class = ClothesSerializer

    # Tìm book theo keyword
    @action(detail=False, methods=['get'], url_path='search/(?P<keyword>[^/.]+)')
    def search(self, request, keyword=''):
        words = keyword.split()
        # Lấy ra danh sách khớp với từ đầu tiên của keyword
        clothes = Clothes.objects.filter(Q(name__icontains=words[0]) | Q(slug__icontains=words[0]) | Q(description__icontains=words[0])).order_by('name')
        # Tiếp tục lặp các từ còn lại
        for word in words:
            clothes = clothes.filter(Q(name__icontains=word) | Q(slug__icontains=word) | Q(description__icontains=word))
        if clothes.exists():
            serializer = ClothesSerializer(clothes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# Get a boọk by slug or id
class ClothesSlugOrIdViewSet(APIView):

    def get(self, request, str):
        try:
            if re.search("\w-", str):
                slug = str
                clothes = Clothes.objects.get(slug=slug, is_active__in=[True])
            else:
                id = str
                clothes = Clothes.objects.get(id=id, is_active__in=[True])
            serializer = ClothesSerializer(clothes)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Clothes.DoesNotExist:
            return Response({'message': 'Not found with provided slug'}, status=status.HTTP_404_NOT_FOUND)


# Get list clothes by category id
class ListClothesOfProducerViewSet(generics.ListAPIView):
    serializer_class = ClothesSerializer

    def get_queryset(self):
        producer_id = self.kwargs['producer_id']
        producer = get_object_or_404(Producer, id=producer_id)
        return producer.clothes.filter(is_active__in=[True]).order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'message': 'No clothes found for this category'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ClothesSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# Get list clothes by style id
class ListClothesOfStyleViewSet(generics.ListAPIView):
    serializer_class = ClothesSerializer

    def get_queryset(self):
        style_id = self.kwargs['style_id']
        style = get_object_or_404(Style, id=style_id)
        return style.clothes.filter(is_active__in=[True]).order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'message': 'No clothes found for this author'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ClothesSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

