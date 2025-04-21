from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email', 'full_name','contact_number','email_verified','contact_number_verified','user_type','date_of_birth','gender','location', 'profile_picture', 'device_id', 'notification_token', 'organization_id']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again.')

        if not user.is_active:
            raise AuthenticationFailed('User is inactive.')

        # Combine user details and tokens into a single object
        user_data = CustomUserSerializer(user).data
        tokens = self.get_tokens(user)

        # Merge tokens with the user data
        user_data.update(tokens)
        return user_data

    @staticmethod
    def get_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','email', 'full_name','contact_number','email_verified','contact_number_verified','user_type','gender','date_of_birth','location', 'profile_picture', 'device_id', 'notification_token']  # Email included for response

    def update(self, instance, validated_data):
        # Update only the allowed fields (exclude 'email')
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.location = validated_data.get('location', instance.location)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.device_id = validated_data.get('device_id', instance.device_id)
        instance.notification_token = validated_data.get('notification_token', instance.notification_token)
        instance.save()

        # Fetch the updated user data
        user_data = CustomUserSerializer(instance).data

        # Add JWT tokens to the response
        tokens = self.get_tokens(instance)
        user_data.update(tokens)  # Combine the user data with JWT tokens

        return user_data

    @staticmethod
    def get_tokens(user):
        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


