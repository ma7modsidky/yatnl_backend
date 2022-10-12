from django.db import models
from django.http import request
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed


from users.models import NewUser
from .exceptions import InvalidUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from django.shortcuts import render

# we will extend the view so the token can have the user iformation we want like; username 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView , RetrieveAPIView
from .serializers import CustomUserSerializer, UpdateUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from .permissions import UpdateUserPermission
from rest_framework.parsers import FormParser, MultiPartParser

# Create your views here.
class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.user_name
        token['email']= user.email
        token['phone'] = user.phone
        # token['name'] = user.first_name + " " +user.last_name
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['about'] = user.about
        

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            raise InvalidUser(e.args[0])
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UpdateUser(UpdateAPIView):
    # def get_serializer_context(self):
    #     print(self.request.FILES)
    #     return super().get_serializer_context()
    queryset = NewUser.objects.all()
    serializer_class = UpdateUserSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [UpdateUserPermission]
    

class UserDetail(RetrieveAPIView):
    queryset = NewUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]
