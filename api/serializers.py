from django.db.models import fields
from django.http import response
from rest_framework import serializers
from api.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=3)
    last_name = serializers.CharField(max_length=255, min_length=3)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('Email is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'roles', 'is_verified']

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields= ['title', 'description']
        
