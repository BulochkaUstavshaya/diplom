from rest_framework import serializers
from .models import Clothes, SetOfClothes

class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ['name_Clothes', 'type_Clothes', 'description', 'price', 'link_Image', 'link_Source']

        def create(self, validated_data):
            return Clothes.objects.create(**validated_data)

class SetOfClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetOfClothes
        fields = ['users', 'id']

        def create(self, validated_data):
            return SetOfClothes.objects.create(**validated_data)