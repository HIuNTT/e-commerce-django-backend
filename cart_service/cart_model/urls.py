from django.urls import path

from .views import AddToCartViewSet, DeleteCartItemViewSet, CartViewSet, UpdateCartItem

urlpatterns = [
    path('add/', AddToCartViewSet.as_view()),
    path('delete/<int:product_id>/', DeleteCartItemViewSet.as_view()),
    path('show/', CartViewSet.as_view()),
    path('update/', UpdateCartItem.as_view()),
]