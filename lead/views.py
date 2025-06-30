from sqlite3 import DatabaseError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from lead.serializers import LeadReminderSerializer, LeadSerializer, LeadCardSerializer, CallLogsSerializer
from .models import Lead, CallLogs
from lead.models import LeadFollowUp, LeadSource, LeadStatus,LeadGender
from .models import LeadReminder, LeadReminderGuest
from accounts.models import CustomUser
from rest_framework.pagination import PageNumberPagination
import json
from utils.color_prints import ColorPrintUtils
from django.db.models import F
from utils.response import success_response, error_response
from .swagger_schemas import get_lead_schema, add_lead


@api_view(['GET'])
def lead_initial_data(request):
    try:
        lead_sources = LeadSource.objects.filter(organization=1).values('id', 'name')
        lead_statuses = LeadStatus.objects.filter(organization=1).values('id', 'name', 'name_alias')
        lead_genders = LeadGender.objects.filter(organization=1).values('id', 'name')
        lead_follow_ups = LeadFollowUp.objects.filter(organization=1).values('id', 'name')

        return success_response(
            data={
                "lead_sources": list(lead_sources),
                "lead_statuses": list(lead_statuses),
                "lead_genders": list(lead_genders),
                "lead_follow_ups": list(lead_follow_ups),
            },
            status_code=200,
            message='Successfully Fetched',
        )

    except DatabaseError as e:
        return error_response(
            message='Database error occurred: ' + str(e),
            status_code=500
        )
    except Exception as e:
        return error_response(
            message='Something went wrong: ' + str(e),
            status_code=500,
            
        )

@add_lead
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lead(request):
    user = request.user
    if request.method == 'POST':
        data = request.data.copy()
        contact_number = data.get('contact_number')
        organization = data.get('organization')  # or adjust according to your model

        # Check for existing lead
        if Lead.objects.filter(contact_number=contact_number, organization=organization).exists():
            return error_response("Lead with this contact number already exists.")

        data['created_by'] = user.id
        data['updated_by'] = user.id

        serializer = LeadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message='success', data=serializer.data)
        return error_response(serializer.errors)


@api_view(['GET'])
def get_all_leads(request):
    leads = Lead.objects.all()
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(leads, request)
    serializer = LeadSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_lead(request, lead_id):
    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        return error_response(message='Lead not found')

    serializer = LeadSerializer(lead)
    return success_response(data=serializer.data, message='Successfully get')

@get_lead_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_lead_cards(request):
    user = request.user
    user_id = user.id
    user_type = user.user_type
    organization = user.organization

    lead_status_parse = []
    try:
        lead_status = request.query_params.get('lead_status')
        if lead_status:
            lead_status_parse = json.loads(lead_status)
    except json.JSONDecodeError:
        lead_status_parse = []

    try:
        # Base queryset (unfiltered)
        if user_type == 'Admin':
            base_leads = Lead.objects.filter(organization=organization)
        elif user_type == 'Telecaller':
            base_leads = Lead.objects.filter(assigned=user_id)
        else:
            return error_response(message="Unauthorized user type")

        # ✅ Count statuses BEFORE any filtering
        status_map = {
            "fresh": "Fresh",
            "follow": "Follow Up",
            "won": "Won",
            "re-enquired": "Re-Enquired",
            "close": "Close",
        }

        status_counts = {}
        for key, status_name in status_map.items():
            count = base_leads.filter(lead_status__name__iexact=status_name).count()
            status_counts[key] = count

        # ✅ Now apply lead_status filter if needed (only for the list)
        leads = base_leads
        if lead_status_parse:
            leads = leads.filter(lead_status__in=lead_status_parse)

        leads = leads.order_by("-updated_on")

        # Paginate and serialize
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(leads, request)
        serializer = LeadCardSerializer(result_page, many=True)
        paginated_data = paginator.get_paginated_response(serializer.data).data

        # Merge counts with paginated data
        response_data = {
            **status_counts,
            **paginated_data,
        }

        return success_response(data=response_data)

    except Exception as e:
        ColorPrintUtils.error_print(e)
        return error_response(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_lead(request, lead_id):
    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        return error_response(message='Lead not found')
    except DatabaseError:
        return error_response(message='Database error occurred')
    
    data = request.data.copy()
    new_contact_number = data.get('contact_number')
    organization = data.get('organization') or lead.organization_id  # fallback if not in request

    # ✅ Check for duplicate only if contact number is changing
    if new_contact_number and new_contact_number != lead.contact_number:
        if Lead.objects.filter(
            contact_number=new_contact_number,
            organization=organization
        ).exclude(pk=lead.pk).exists():
            return error_response("Lead with this contact number already exists.")

    # Automatically set the user who updated the lead
    data['updated_by'] = request.user.id
    data.pop('created_by', None)

    serializer = LeadSerializer(lead, data=data, partial=True)

    try:
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data)
        else:
            return error_response(message=serializer.errors)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lead(request, lead_id):
    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        print("yaha")
        return error_response(message='Lead Not Found')
    except DatabaseError:
        return error_response(message='Database error occurred')

    try:
        lead.delete()
        return success_response({'detail': 'Lead deleted successfully'})
    except Exception as e:        
        return error_response(message=str(e))


@api_view(['POST'])
def add_call_log(request):
    serializer = CallLogsSerializer(data=request.data)
    if serializer.is_valid():
        lead = serializer.validated_data.get('lead_id')
        serializer.save(organization=lead.organization)
        return Response({
            "message": "Call log added successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Lead Reminder API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lead_reminder(request):
    serializer = LeadReminderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return success_response(message='message', data=serializer.data)
    return error_response(message=serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lead_reminder(request, pk):
    reminder = get_object_or_404(LeadReminder, pk=pk)
    reminder.delete()
    return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_reminder(request):
    try:
        query = request.query_params
        lead_id = query.get('lead_id')

        user = request.user
        user_id = user.id
        user_type = user.user_type
        organization = user.organization

        # Fetch reminders based on user role or lead_id
        if lead_id:
            reminders = LeadReminder.objects.filter(lead_id=lead_id).order_by('-created_on')
        else:
            if user_type == 'Admin':
                reminders = LeadReminder.objects.filter(organization=organization).order_by('-created_on')
            elif user_type == 'Telecaller':
                reminders = LeadReminder.objects.filter(created_by=user_id).order_by('-created_on')
            else:
                return error_response(message="Unauthorized user type")

        # Paginate the queryset
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Default page size; you can allow dynamic via query param
        paginated_reminders = paginator.paginate_queryset(reminders, request)
        serializer = LeadReminderSerializer(paginated_reminders, many=True)

        # Custom formatted response
        paginated_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data
        }

        return success_response(data=paginated_data, message="Successfully fetched reminders")
    
    except Exception as e:
        return error_response(message=f"An error occurred: {str(e)}")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lead_bulk_add(request):
    user = request.user
    data = request.data.copy()
    leads_data = data.get('leads', [])

    if not leads_data:
        return error_response(message='No leads data provided')

    organization_id = user.organization.id

    stats = {
        "total_leads": len(leads_data),
        "inserts": 0,
        "duplicate": 0,
        "rejected": 0
    }

    for lead_data in leads_data:
        # Add metadata
        lead_data['created_by'] = user.id
        lead_data['updated_by'] = user.id
        lead_data['organization'] = organization_id
        

        if not lead_data.get('assigned'):
            lead_data['assigned'] = user.id

        contact_number = lead_data.get('contact_number')
        is_duplicate = False

        if contact_number:
            if Lead.objects.filter(organization_id=organization_id, contact_number=contact_number).exists():
                stats['duplicate'] += 1
                is_duplicate = True

        if is_duplicate:
            continue

        serializer = LeadSerializer(data=lead_data)
        if serializer.is_valid():
            serializer.save()
            stats['inserts'] += 1
        else:
            stats['rejected'] += 1

    return success_response(data=stats, message='Bulk lead operation summary')


    