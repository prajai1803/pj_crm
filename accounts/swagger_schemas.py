from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import LoginSerializer, UpdateUserSerializer


login_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(
                type=openapi.TYPE_STRING, 
                default='prajai1801@gmail.com',
                description='User email'
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING, 
                default='prakhar02',
                description='User password'
            ),
        },
    ),
    operation_summary="Login user",
    operation_description="Logs in a user with email and password and returns access/refresh tokens.",
    responses={
        200: "Login succeeded or failed",
        400: "Validation error",
        500: "Server error"
    }
)

update_profile_schema = swagger_auto_schema(
    method='put',
    request_body=UpdateUserSerializer,
    operation_summary="Update Profile",
    operation_description="Updates a user's profile.",
    responses={
        200: "Update Success",
        400: "Validation error",
        500: "Server error"
    },
    security=[{'Bearer': []}],  # 👈 tells Swagger to use Bearer Auth
)
