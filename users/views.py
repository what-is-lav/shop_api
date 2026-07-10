from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random

from .serializers import UserRegisterSerializer, UserConfirmSerializer
from .models import Verifications 


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')    
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )
    
    code = str(random.randint(100000, 999999))
    Verifications.objects.create(user=user, code=code)
    
    return Response(
        data={'user_id': user.id, 'code': code}, 
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def confirm_api_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    code = serializer.validated_data.get('code')
    
    try:
        confirm_code = Verifications.objects.get(code=code)
    except Verifications.DoesNotExist:
        return Response(
            data={'error': 'Invalid or expired code!'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    user = confirm_code.user
    user.is_active = True
    user.save()
    
    confirm_code.delete()
    
    return Response(
        data={'message': 'User account activated successfully!'}, 
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def authorization_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
        
    return Response(
        data={'error': 'Invalid credentials or account is not active.'},
        status=status.HTTP_401_UNAUTHORIZED
    )

# Create your views here.
