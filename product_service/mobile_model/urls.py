from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MobileViewSet, MobileSlugOrIdViewSet, ListMobilesOfProducerViewSet

router = DefaultRouter()
router.register('', MobileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:str>/', MobileSlugOrIdViewSet.as_view()),
    path('producer/<int:producer_id>/', ListMobilesOfProducerViewSet.as_view()),
]