from django.shortcuts import render
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Account
from .serializers import AccountRegisSerializer


# Create your views here.


class RegisterAccountAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountRegisSerializer
    permission_classes = [permissions.AllowAny]





