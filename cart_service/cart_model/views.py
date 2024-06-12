import requests
from django.shortcuts import render, get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem
from .serializers import CartItemSerializer


# Create your views here.


class AddToCartViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        product_id = request.data.get('product_id')
        product_type = request.data.get('product_type')
        data = {
            'user_id': user_id,
            'product_id': product_id,
            'product_type': product_type,
        }
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            cart_item, created = CartItem.objects.get_or_create(user_id=user_id, product_id=product_id, product_type=product_type)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return Response({'message': 'Product added to cart'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCartItemViewSet(APIView):
    def delete(self, request, product_id):
        cart_item = get_object_or_404(CartItem, user_id=request.user.id, product_id=product_id)
        cart_item.delete()
        return Response({'message': 'CartItem deleted!'}, status=status.HTTP_204_NO_CONTENT)


class CartViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        cart_items = CartItem.objects.filter(user_id=request.user.id)
        total_price = 0
        item_count = 0
        cart_item_data = []

        for cart_item in cart_items:
            product = self.get_product(cart_item.product_type, cart_item.product_id)
            if product:
                price = float(product.get('price'))
                cart_item_data.append({
                    'quantity': cart_item.quantity,
                    'item': product,
                    'line_price': cart_item.quantity * price,
                })
                item_count += cart_item.quantity
                total_price += cart_item.quantity * price
        response_data = {
            'item_count': item_count,
            'items': cart_item_data,
            'total_price': total_price,
            'user_id': request.user.id,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    def get_product(self, product_type, product_id):
        if product_type == 'book':
            url = 'http://127.0.0.1:8002/book/{}'.format(product_id)
        if product_type == 'mobile':
            url = 'http://127.0.0.1:8002/mobile/{}'.format(product_id)
        if product_type == 'clothes':
            url = 'http://127.0.0.1:8002/clothes/{}'.format(product_id)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None


class UpdateCartItem(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        product_id = request.data.get('product_id')
        product_type = request.data.get('product_type')
        cart_item = CartItem.objects.get(user_id=user_id, product_id=product_id, product_type=product_type)
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
            return Response({'message': 'CartItem updated'}, status=status.HTTP_200_OK)