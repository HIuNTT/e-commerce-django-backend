import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.


class SearchViewSet(APIView):
    def get(self, request):
        key = request.query_params.get('key')
        if key:
            result = {
                'books': self.search_book(key),
                'mobiles': self.search_mobile(key),
                'clothes': self.search_clothes(key),
            }
            return Response(data=result, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Please enter keyword'}, status=status.HTTP_400_BAD_REQUEST)

    def search_book(self, key):
        book_service_url = 'http://127.0.0.1:8002/book/search/{}'.format(key)
        book_response = requests.get(book_service_url)
        if book_response.status_code == 200:
            return book_response.json()
        return []

    def search_mobile(self, key):
        mobile_service_url = 'http://127.0.0.1:8002/mobile/search/{}'.format(key)
        mobile_response = requests.get(mobile_service_url)
        if mobile_response.status_code == 200:
            return mobile_response.json()
        return []

    def search_clothes(self, key):
        clothes_service_url = 'http://127.0.0.1:8002/clothes/search/{}'.format(key)
        clothes_response = requests.get(clothes_service_url)
        if clothes_response.status_code == 200:
            return clothes_response.json()
        return []

