from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Contact

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'dob', 
            'is_pro'
        )


class ContactSerializer(serializers.ModelSerializer):

    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner_firstname = serializers.ReadOnlyField(source='owner.first_name')
    owner_lastname = serializers.ReadOnlyField(source='owner.last_name')
    following_username = serializers.ReadOnlyField(source='following.username')
    following_firstname = serializers.ReadOnlyField(source='following.first_name')
    following_lastname = serializers.ReadOnlyField(source='following.last_name')
    
    class Meta:
        model = Contact
        fields = (
            'id',
            'owner',
            'following',
            'owner_username',
            'owner_firstname',
            'owner_lastname',
            'following_username',
            'following_firstname',
            'following_lastname'
        )


