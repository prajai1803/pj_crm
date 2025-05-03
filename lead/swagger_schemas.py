from drf_yasg.utils import swagger_auto_schema
from .serializers import CallLogsSerializer, LeadCardSerializer, LeadSerializer
from drf_yasg import openapi


call_log_create = swagger_auto_schema(
    method='put',
    request_body=CallLogsSerializer,
    operation_summary="Update Profile",
    operation_description="Updates a user's profile.",
    responses={
        200: "Update Success",
        400: "Validation error",
        500: "Server error"
    },
    security=[{'Bearer': []}],
)

add_lead = swagger_auto_schema(
    method='post',
    request_body=LeadSerializer,
    operation_summary="Create Lead",
    operation_description="Updates a user's profile.",
    responses={
        200: "Update Success",
        400: "Validation error",
        500: "Server error"
    },
    security=[{'Bearer': []}],
)


get_lead_schema = swagger_auto_schema(
    method='get',
    operation_summary="Fetch Lead Cards",
    operation_description="Fetch Lead only those values shown in the card",
    responses={
        200: openapi.Response(description="Fetch Success"),
        400: openapi.Response(description="Validation Error"),
        500: openapi.Response(description="Server Error"),
    },
    security=[{'Bearer': []}],
)


