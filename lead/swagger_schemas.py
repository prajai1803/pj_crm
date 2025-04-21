from drf_yasg.utils import swagger_auto_schema
from .serializers import CallLogsSerializer




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
