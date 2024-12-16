from sqlite3 import DatabaseError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from lead.serializers import LeadSerializer,LeadCardSerializer
from .models import Lead
from rest_framework.pagination import PageNumberPagination

@api_view(['GET'])
def lead_dropdowns(request):
    data = {
        'lead_sources': [{'id': source[0], 'name': source[1]} for source in Lead.LEAD_SOURCES],
        'lead_statuses': [{'id': status[0], 'name': status[1]} for status in Lead.LEAD_STATUSES],
        'genders': [{'id': gender[0], 'name': gender[1]} for gender in Lead.GENDER_CHOICES],
        'centers': [{'id': center[0], 'name': center[1]} for center in Lead.CENTER_CHOICES],
    }
    return Response(data)

@api_view(['GET'])
def get_all_leads(request):
    leads = Lead.objects.all()
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(leads, request)
    serializer = LeadSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_lead_cards(request):
    leads = Lead.objects.all().order_by('-updated_on')
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(leads, request)
    serializer = LeadCardSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lead(request):
    user = request.user
    if request.method == 'POST':
        data = request.data.copy()
        data['created_by'] = user.id
        data['updated_by'] = user.id
        
        serializer = LeadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_lead(request, lead_id):
    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        return Response({'detail': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
    except DatabaseError:
        return Response({'detail': 'Database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Automatically set the user who updated the lead
    request.data['updated_by'] = request.user.id
    request.data.pop('created_by', None)
    serializer = LeadSerializer(lead, data=request.data, partial=True)


    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lead(request, lead_id):
    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        return Response({'detail': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
    except DatabaseError:
        return Response({'detail': 'Database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        lead.delete()
        return Response({'detail': 'Lead deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
