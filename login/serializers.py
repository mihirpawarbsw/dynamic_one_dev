# myapp/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserAuthentication

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email','first_name']  # Add any other fields you need

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Set the password
        user.save()
        return user



# Serializer for the UserAuthentication model
class UserAuthenticationSerializer(serializers.ModelSerializer):
    # To display related user's data (like user_id and email) from the User model
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # Include user ID from User model
    user_email = serializers.EmailField(source='user.email', read_only=True)  # Include email from User model

    class Meta:
        model = UserAuthentication
        fields = ['user_id', 'user_email', 'email', 'token']
