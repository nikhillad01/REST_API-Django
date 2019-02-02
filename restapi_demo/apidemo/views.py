from django.http import HttpResponse, HttpRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.backends import django
from django.urls import reverse
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import stock,Registration  # imports the models
from .models import RestRegistration
from .serializers import stockSerializer
from .forms import Registrationform
from django.contrib.auth import get_user_model, authenticate
import jwt,json
from rest_framework.response import Response
from .serializers import TokenAuthentication
from .serializers import registrationSerializer
from rest_framework.generics import CreateAPIView

from jinja2 import Environment,PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('apidemo', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def index(request):         # this is homepage.
    return render(request, 'index.html', {})
def login(request):
    return  render(request,'rest_framework/login.html',{})
def dash(request):      # /dash/
    return render(request,'dashboard.html',{})


User= get_user_model()          # will retrieve the USER model class.
import re

class UserCreateAPI(CreateAPIView):             # Registration using Rest framework Using User Model.

    serializer_class=registrationSerializer
    queryset = User.objects.all()                  # fields according to User   (adds data to USER model)
    #queryset = RestRegistration.objects.all()   # # fields according to RestRegistration model.
#     def post(self, request):
#         email=request.data['email']
#         match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
#         try:
#             if match == None:
#                 #print('Bad Syntax')
#                 # raise ValueError('Bad Syntax')
#                 return Response('Please enter valid Email')
#             else:obj.proceed()
#                 return Response("Valid")
#         except ValueError:
#             print('Not Valid Email')
#
#     def proceed(self):
#         serializer_class = registrationSerializer
#         queryset = User.objects.all()
#
#         #registrationSerializer
# obj=UserCreateAPI()
from django.contrib.auth.hashers import PBKDF2PasswordHasher
class LoginView(APIView):
    hasher = PBKDF2PasswordHasher()

    serializer_class = TokenAuthentication
    queryset = User.objects.all()
    http_method_names = ['post', 'get']      # to use POST method by default it was using GET.


    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    #login(user)
                    payload = {'username': username,
                                'password': password,}


                    jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256')}
                                                                            # generates the token using payload information.

                            #template = env.get_template('dashboard.html')   # using Jinja2 to get the dashboard template

                    #template.render(username=username)             # renders to template with variable username.

                    #return render_template()
                    return HttpResponse(
                     #jwt_token,
                    #user.username,
                     jwt_token.values(),
                        #json.dumps(list(jwt_token['token'])),
                        #json.dumps(jwt.decode(jwt_token)),
                        status=200,
                        content_type="application/json"
                    )
                    #return HttpResponseRedirect(reverse('rest_register'))
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username, password))
                    return HttpResponse("Invalid login details given")

        else:
            return render(request, 'dashboard.html', {})
    ############################
        # if not request.data:    # if nothing is provided in username and password.
        #     return Response({'Error': "Please provide username/password"}, status="400")
        # # used Rest Requests request.data instead of request.POST , can be compatible with POST,PUT etc
        # username = request.data['username']     # gets the username
        # password = request.data['password']     # gets the password
        # try:
        #     user = User.objects.get(username=username, password=password)   # Checks for Valid username and password.
        #   #  user=authenticate(username=username, password=password)
        # except User.DoesNotExist:
        #     return Response({'Error': "Invalid username or password"}, status="400")
        # # status 400 Bad Request.
        # if user:
        #         payload = {
        #             'username': user.username,
        #             'password': user.password,
        #         }
        #         jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256')}
        #                                                         # generates the token using payload information.
        #         # print(jwt_token)
        #
        #         template = env.get_template('dashboard.html')   # using Jinja2 to get the dashboard template
        #
        #         #template.render(username=username)             # renders to template with variable username.
        #
        #         #return render_template()
        #         return HttpResponse(
        #             #jwt_token,
        #             #user.username,
        #             jwt_token.values(),
        #             #json.dumps(list(jwt_token['token'])),
        #             #json.dumps(jwt.decode(jwt_token)),
        #             status=200,
        #             content_type="application/json"
        #         )
        # else:
        #     return Response(
        #         json.dumps(list({'Error': "Invalid credentials"})),
        #         status=400,
        #         content_type="application/json"
        #     )
#%###########################################################
from django import forms
# class register_with_confirm_password(forms.ModelForm,CreateAPIView):
#
#     http_methods=['post','get']
#     password=forms.CharField(widget=forms.PasswordInput())
#     confirm_password=forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model=User
#         fields=('username','email','password')
#
#     def clean(self):
#         cleaned_data = super(register_with_confirm_password, self).clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#
#         if password != confirm_password:
#             raise forms.ValidationError(
#                 "password and confirm_password does not match"
#             )

from django.contrib.auth import logout

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    def post(self,request):
        #logout()
        #TokenAuthentication.authenticate()
        return Response(status=204)


from django_filters import rest_framework as filters

import requests
from .forms import LoginForm
class user_login(ModelViewSet):
    serializer_class=TokenAuthentication
    renderer_classes = ['TemplateHTMLRenderer']
    template_name = 'api.html'
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('completed',)
    ordering = ('-date_created',)


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False      # user disabled
            user.save()                 # stores in database.
            message = render_to_string('acc_active_email.html', {
                # render_to_string()  takes two arguments 1.page to load and render and 2. Context {}for loading
                'user': user,
                #http://127.0.0.1:8000
                #'domain':current_site.domain,
                'domain':'http://127.0.0.1:8000',
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),  # coz django 2.0.0
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your Fundoo account.'  # mail subject
            to_email = form.cleaned_data.get('email')       # mail id to be sent to
            email = EmailMessage(mail_subject, message, to=[to_email])   # takes 3 args: 1. mail subject 2. message 3. mail id to send
            email.send()        # sends the mail
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print('Uid:             :',uid)
        user = User.objects.get(pk=uid)     # gets the username
        print('user:::::',user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        #return render(request, 'rest_login/')
        return HttpResponsePermanentRedirect(reverse('rest_login'))
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return render(request, 'login.html', {'form': form})
    else:
        return HttpResponse('Activation link is invalid!')

def login(request):
    return render(request, 'dashboard.html')

