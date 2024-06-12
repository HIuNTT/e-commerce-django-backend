from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClothesViewSet, ClothesSlugOrIdViewSet, ListClothesOfProducerViewSet, ListClothesOfStyleViewSet

router = DefaultRouter()
router.register('', ClothesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:str>/', ClothesSlugOrIdViewSet.as_view()),
    path('producer/<int:producer_id>/', ListClothesOfProducerViewSet.as_view()),
    path('style/<int:style_id>/', ListClothesOfStyleViewSet.as_view()),
]