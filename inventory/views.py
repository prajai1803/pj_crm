from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product
from utils.response import success_response, error_response
from .serializers import CategorySerializer, ProductFetchSerializer, ProductSerializer


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    try:
        user = request.user
        data = request.data.copy()        
        organization_id = user.organization.id
        print("User organization ID:", organization_id)
        data['organization'] = user.organization.id if user.organization else None
        print("Data being saved:", data)

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data)
        return error_response(serializer.errors)
    
    except Exception as e:
        print(f"Error occurred while creating category: {e}")
        return error_response({'detail': 'An unexpected error occurred.'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return error_response({'error': 'Category not found'})

    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return success_response(message="Success", data= serializer.data)
    return error_response(serializer.errors)

@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return error_response(message="Category not found")

    category.delete()
    return success_response(message="Category deleted successfully")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_categories(request):
    user = request.user
    organization = getattr(user, 'organization', None)  # adjust this line as per your user-org relation

    if not organization:
        return error_response(message="User does not belong to any organization.", status=403)

    categories = Category.objects.filter(organization=organization)
    serializer = CategorySerializer(categories, many=True)
    return success_response(message="Successfully fetched", data=serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_product(request):
    try:
        user = request.user
        organization = getattr(user, 'organization', None)
        
        if not organization:
            return error_response('User does not belong to any organization.')

        # Order products by created_at descending
        products = Product.objects.filter(organization=organization).order_by('-created_at')
        serializer = ProductFetchSerializer(products, many=True)
        
        return success_response(data=serializer.data)

    except Exception as e:
        return error_response(message=f'{e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    try:
        user = request.user
        data = request.data.copy()

        if not hasattr(user, 'organization') or user.organization is None:
            return error_response({'error': 'User does not belong to any organization.'}, status=status.HTTP_400_BAD_REQUEST)

        organization_id = user.organization.id
        data['organization'] = organization_id

        print("User organization ID:", organization_id)
        print("Data being saved:", data)

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data)
        return error_response(message=serializer.errors)

    except Exception as e:
        print(f"Error while creating product: {e}")
        return error_response(message=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    try:
        product = Product.objects.get(id=pk)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Product updated successfully.")
        else:
            return error_response(message="Validation failed.", data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return error_response(message="Product not found.")

    except Exception as e:
        return error_response(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    try:
        product = Product.objects.get(id=pk)

        product.delete()
        return success_response(message="Successfully Deleted")

    except Product.DoesNotExist:
        return error_response(message="Product not found.")

    except Exception as e:
        return error_response(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


