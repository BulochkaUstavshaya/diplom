from rest_framework import serializers
from .models import UserClothes

class UserClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClothes
        fields = ['nameClothes', 'typeClothes', 'description', 'price', 'linkImage', 'linkSource']

        def create(self, validated_data):
            return UserClothes.objects.create(**validated_data)