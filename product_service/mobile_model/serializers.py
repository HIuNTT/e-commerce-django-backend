from rest_framework import serializers
from .models import Producer, Mobile


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name']


class MobileSerializer(serializers.ModelSerializer):
    brand = ProducerSerializer(read_only=True)

    class Meta:
        model = Mobile
        fields = '__all__'

