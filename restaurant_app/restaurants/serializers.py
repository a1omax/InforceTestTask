from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import Restaurant, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'id',
            'restaurant',
            'date',
            'items',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Menu.objects.all(),
                fields=['restaurant', 'date'],
                message='Restaurant and date must be unique'
            )
        ]

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)


class RestaurantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        min_length=1,
        max_length=200,
        validators=[
            UniqueValidator(queryset=Restaurant.objects.all(), message="Restaurant name should be unique")
        ])

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'address',
        ]


class TodayMenusSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = Menu
        fields = [
            'id',
            'restaurant',
            'items',
        ]
