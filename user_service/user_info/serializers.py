from rest_framework import serializers

from user_model.models import User

from user_model.models import Account

from user_model.models import Fullname

from user_model.models import Address


class FullnameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fullname
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class AccountInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'mobile_number']


class UserInfoSerializer(serializers.ModelSerializer):
    account = AccountInfoSerializer()
    full_name = FullnameSerializer()
    address = AddressSerializer()

    class Meta:
        model = User
        fields = '__all__'

