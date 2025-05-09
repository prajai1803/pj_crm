from rest_framework.response import Response
from utils.color_prints import ColorPrintUtils

def success_response(message="Success", data=None, status_code=200):
    return Response({
        "success": True,
        "message": message,
        "data": data or {}
    }, status=status_code)

def error_response(message="Error", data=None, status_code=200):
    ColorPrintUtils.error_print(message)
    return Response({
        "success": False,
        "message": message,
        "data": data or {}
    }, status=status_code)
