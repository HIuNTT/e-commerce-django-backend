from rest_framework import serializers
from .models import Clothes, Producer, Style


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name']


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ['id', 'name']


class ClothesSerializer(serializers.ModelSerializer):
    category = ProducerSerializer(read_only=True)
    style = StyleSerializer(read_only=True)

    class Meta:
        model = Clothes
        fields = '__all__'

