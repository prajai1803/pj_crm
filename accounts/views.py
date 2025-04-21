from queue import Full
import string
import json
from django.forms import ValidationError
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
from rest_framework.exceptions import AuthenticationFailed
from .swagger_schemas import login_schema, update_profile_schema

from utils.response import error_response, success_response
from .models import CustomUser
import random


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

@login_schema
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        return success_response(message="Login succeeded", data=serializer.validated_data)

    except AuthenticationFailed as e:
        return error_response(message=str(e), data={}, status_code=200)

    except ValidationError as e:
        # Safely get errors from the exception itself
        return error_response(message="Invalid input", data=e.detail, status_code=400)

    except Exception as e:
        # Catch-all for other unexpected errors
        print(e)
        return error_response(message="Something went wrong", data={}, status_code=500)

@update_profile_schema
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    print(user)
    serializer = UpdateUserSerializer(user, data=request.data, partial=True)  # Set partial=True for PATCH requests

    if serializer.is_valid():
        updated_data = serializer.save()  # Save and get the updated data, including tokens
        return Response(updated_data, status=status.HTTP_200_OK)  # Return the updated user data and tokens
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)