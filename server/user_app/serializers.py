from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from django.db.models import Avg

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'confirm_password', 'role', 'first_name', 'last_name', 'eligible_service')
    

    def create(self, validated_data):
        print(f"validated_data: {validated_data}")
        user = CustomUser.objects.create_user(
            email=validated_data.get['email'],
            role=validated_data.get['role'],
            password=validated_data.get['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            eligible_service=validated_data.get('eligible_service', ''),
        )
        return user


class BaseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProfileModel
        fields = "__all__"


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicModel
        fields = "__all__"

class UserRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return RatingModel.objects.filter(rated_user=obj.rated_user).aggregate(Avg('stars'))['stars__avg']

    class Meta:
        model = RatingModel
        fields = "__all__"