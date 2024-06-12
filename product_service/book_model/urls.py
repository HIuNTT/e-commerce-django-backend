from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, BookSlugOrIdViewSet, ListBookOfCategoryViewSet, ListBookOfAuthorViewSet, ListBookOfPublisherViewSet

router = DefaultRouter()
router.register('', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:str>/', BookSlugOrIdViewSet.as_view()),
    path('category/<int:category_id>/', ListBookOfCategoryViewSet.as_view()),
    path('author/<int:author_id>/', ListBookOfAuthorViewSet.as_view()),
    path('publisher/<int:publisher_id>/', ListBookOfPublisherViewSet.as_view()),
]