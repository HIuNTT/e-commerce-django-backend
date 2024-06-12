from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Fullname, Address, Account


class AccountRegisSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Account.objects.all())])
    mobile_number = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Account.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    repeat_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'mobile_number', 'password', 'repeat_password']

    def validate(self, attrs):
        if attrs.get('password') != attrs.pop('repeat_password'):
            raise serializers.ValidationError(
                {'repeat_password': "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        account.set_password(validated_data['password'])
        account.save()
        return account

