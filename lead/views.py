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
