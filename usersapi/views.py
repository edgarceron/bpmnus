"""Views for the usersapi module"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.backends import TokenBackend
from jwt import InvalidTokenError
from core.crud.standard import Crud
from usersapi.business_logic import data_filters
from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['POST'])
def add_user(request):
    """Tries to create a user and returns the result"""
    crud_object = Crud(UserSerializer, User)
    return crud_object.add(request)

@api_view(['PUT'])
def replace_user(request, user_id):
    "Tries to update a user and returns the result"
    crud_object = Crud(UserSerializer, User)
    return crud_object.replace(request, user_id)

@api_view(['POST'])
def get_user(request, user_id):
    "Return a JSON response with user data for the given id"
    crud_object = Crud(UserSerializer, User)
    return crud_object.get(request, user_id)

@api_view(['DELETE'])
def delete_user(request, user_id):
    """Tries to delete an user and returns the result."""
    crud_object = Crud(UserSerializer, User)
    return crud_object.delete(user_id, "Proyecto elminado exitosamente")

@api_view(['POST'])
def list_user(request):
    """Returns a JSON response containing registered user for a datatable"""
    crud_object = Crud(UserSerializer, User)
    return crud_object.listing(request, data_filters.user_listing_filter)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_user_from_token(request):
    key = request.data["token"]
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(key,verify=False)
        user_id = valid_data['user_id']
        user = User.objects.get(pk=user_id)
        serialzied = UserSerializer(user).data.copy()
        data = {"user": serialzied, "user_image": ""}
        return Response(data, status.HTTP_200_OK, content_type='application/json')
    except InvalidTokenError as v:
        user = None
        return Response(user, status.HTTP_204_NO_CONTENT, content_type='application/json')

