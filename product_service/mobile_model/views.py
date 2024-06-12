import re
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Mobile, Producer
from .serializers import MobileSerializer


# Create your views here.


# Get list mobiles, search mobiles by keyword
class MobileViewSet(viewsets.ViewSet,
                  generics.ListAPIView):

    queryset = Mobile.objects.filter(is_active__in=[True])
    serializer_class = MobileSerializer

    # Tìm mobile theo keyword
    @action(detail=False, methods=['get'], url_path='search/(?P<keyword>[^/.]+)')
    def search(self, request, keyword=''):
        words = keyword.split()
        # Lấy ra danh sách khớp với từ đầu tiên của keyword
        mobiles = Mobile.objects.filter(Q(name__icontains=words[0]) | Q(slug__icontains=words[0]) | Q(description__icontains=words[0])).order_by('name')
        # Tiếp tục lặp các từ còn lại
        for word in words:
            mobiles = mobiles.filter(Q(name__icontains=word) | Q(slug__icontains=word) | Q(description__icontains=word))
        if mobiles.exists():
            serializer = MobileSerializer(mobiles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# Get a mobile by slug or id
class MobileSlugOrIdViewSet(APIView):

    def get(self, request, str):
        try:
            if re.search("\w-", str):
                slug = str
                mobile = Mobile.objects.get(slug=slug, is_active__in=[True])
            else:
                id = str
                mobile = Mobile.objects.get(id=id, is_active__in=[True])
            serializer = MobileSerializer(mobile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Mobile.DoesNotExist:
            return Response({'message': 'Not found with provided slug'}, status=status.HTTP_404_NOT_FOUND)


# Get list mobiles by brand id
class ListMobilesOfProducerViewSet(generics.ListAPIView):
    serializer_class = MobileSerializer

    def get_queryset(self):
        producer_id = self.kwargs['producer_id']
        producer = get_object_or_404(Producer, id=producer_id)
        return producer.mobiles.filter(is_active__in=[True]).order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'message': 'No mobile found for this brand'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MobileSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

