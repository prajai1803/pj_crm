from queue import Full
import string
import json
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import CustomUserSerializer, LoginSerializer, UpdateUserSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from .models import CustomUser
import random



def generate_otp(length=6):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request, user_id):
    user = get_object_or_404(CustomUser, user_id=user_id)
    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def refresh_token(request):
    serializer = TokenRefreshSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    serializer = UpdateUserSerializer(user, data=request.data, partial=True)  # Set partial=True for PATCH requests

    if serializer.is_valid():
        updated_data = serializer.save()  # Save and get the updated data, including tokens
        return Response(updated_data, status=status.HTTP_200_OK)  # Return the updated user data and tokens
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)