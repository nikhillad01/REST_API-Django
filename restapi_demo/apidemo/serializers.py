from django.forms import forms
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .models import stock,Registration
from django.contrib.auth import get_user_model
# serializers used to convert models into JSON .
from django.contrib.contenttypes.models import ContentType
User= get_user_model()
from rest_framework import status,exceptions
from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.contrib.auth.models import User
import jwt
from .models import RestRegistration
import json
from rest_framework.serializers import (HyperlinkedIdentityField,ModelSerializer,SerializerMethodField,ValidationError)
class stockSerializer(serializers.ModelSerializer):


    class Meta:
        model = stock
        fields = '__all__'
        # or
        #fields =('ticker','volume','open','close')# if we want only specific values from models


class registrationSerializer(serializers.ModelSerializer):
    # model = Registration
    # fields='__all__'
    username=serializers.CharField(max_length=20)
    password=serializers.CharField( style={'input_type': 'password'})
    email=serializers.EmailField()
    class Meta:

        model = User                    # Database Model to  store the data in .
       # model=RestRegistration         # Stores data in  registration model.
        #fields='__all__'               # fields used as queryset.
        fields=['username',
                'password',
                'email']


from django.contrib.auth import authenticate
from rest_framework import  exceptions
#class loginSerializer(serializers.Serializer):
    # username=serializers.CharField()
    # password=serializers.CharField()
    # def valid(self, data):
    #     username=data.get("username","")
    #     password=data.get("password","")
    #
    #     if username and password:
    #         user=authenticate(username=username,password=password)
    #         if user:
    #             if user.is_active:
    #                 data['user']=user
    #             else:
    #                 msg='user is deactivated'
    #                 raise exceptions.ValidationError(msg)
    #         else:
    #             msg='wrong Login details'
    #             raise exceptions.ValidationError(msg)
    #     else:
    #         msg='must provide username and password both'
    #         raise exceptions.ValidationError(msg)
    #     return data



class TokenAuthentication(BaseAuthentication, serializers.ModelSerializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(style={'input_type': 'password'})
   # confirm_password=serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['username',
                  'password']
        def get_model(self):
            return User

        # def authenticate(self, request):
        #     auth = get_authorization_header(request).split()
        #     if not auth or auth[0].lower() != b"token":
        #         return None
        #
        #     if len(auth) == 1:
        #         msg = 'Invalid token header. No credentials provided.'
        #         raise exceptions.AuthenticationFailed(msg)
        #     elif len(auth) > 2:
        #         msg = 'Invalid token header'
        #         raise exceptions.AuthenticationFailed(msg)
        #
        #     try:
        #         token = auth[1]
        #         if token == "null":
        #             msg = 'Null token not allowed'
        #             raise exceptions.AuthenticationFailed(msg)
        #     except UnicodeError:
        #         msg = 'Invalid token header. Token string should not contain invalid characters.'
        #         raise exceptions.AuthenticationFailed(msg)
        #
        #     return self.authenticate_credentials(token)

        def authenticate_credentials(self, token):
            #model = self.get_model()
            payload = jwt.decode(token, "SECRET_KEY",algorithm='HS256')     # decodes the token
            username = payload['username']      # gets username from decoded token
            password = payload['password']      # gets password from decoded token
            msg = {'Error': "Token mismatch", 'status': "401"}
            try:

                user = User.objects.get(
                    username=username,
                    password=password,
                    is_active=True
                )

                if not user.token['token'] == token:
                    raise exceptions.AuthenticationFailed(msg)

            except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
                return HttpResponse({'Error': "Token is invalid"}, status="403")
            except User.DoesNotExist:
                return HttpResponse({'Error': "Internal server error"}, status="500")

            return (user, token)

        def authenticate_header(self, request,token):
            return  token