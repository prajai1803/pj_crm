from rest_framework.response import Response

def success_response(message="Success", data=None, status_code=200):
    return Response({
        "success": True,
        "message": message,
        "data": data or {}
    }, status=status_code)

def error_response(message="Error", data=None, status_code=200):
    return Response({
        "success": False,
        "message": message,
        "data": data or {}
    }, status=status_code)
