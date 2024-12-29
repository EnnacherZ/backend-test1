from rest_framework import serializers
from .models import *


class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = '__all__'

class ShoeDetailSerializer(serializers.ModelSerializer):
    size = serializers.CharField(source = 'size', read_only=True)
    class Meta:
        model = ShoeDetail
        fields = '__all__'

class SandalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sandal
        fields = '__all__'

class SandalDetailSerializer(serializers.ModelSerializer):
    size = serializers.CharField(source = 'size', read_only=True)
    class Meta:
        model = SandalDetail
        fields = '__all__'


class ShirtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shirt
        fields = '__all__'

class ShirtDetailSerializer(serializers.ModelSerializer):
    size = serializers.CharField(source = 'size', read_only=True)
    class Meta:
        model = ShirtDetail
        fields = '__all__'

class PantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pant
        fields = '__all__'

class PantDetailSerializer(serializers.ModelSerializer):
    size = serializers.CharField(source = 'size', read_only=True)
    class Meta:
        model = PantDetail
        fields = '__all__'