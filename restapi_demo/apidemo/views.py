from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.backends import django
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import stock,Registration  # imports the models
from .models import RestRegistration
from .serializers import stockSerializer
from .forms import Registrationform
from django.contrib.auth import get_user_model
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

def dash(request):      # /dash/
    return render(request,'dashboard.html',{})


class StockList(APIView):       # /stocks/


    def get(self,request):
        stocks=stock.objects.all()      # using fields from stock model.
        serializer = stockSerializer(stocks)

        return Response(serializer.data)


    def post(self):
        pass


def register(request):              # Normal Registration without Rest Framework.

    form = Registrationform(request.POST or None)
    if form.is_valid():
        form.save()
    context ={
        'form': form
    }

    return render(request, 'registration.html', context)



User= get_user_model()          # will retrieve the USER model class.

class UserCreateAPI(CreateAPIView):             # Registration using Rest framework Using User Model.

    serializer_class=registrationSerializer
    queryset = User.objects.all()          # fields according to User   (adds data to USER model)
    #queryset = RestRegistration.objects.all()   # # fields according to RestRegistration model.
                                                # (adds data to RestRegistration Model.)
    #registrationSerializer

class LoginView(APIView):

    serializer_class = TokenAuthentication
    queryset = User.objects.all()
    http_method_names = ['post', 'get']      # to use POST method by default it was using GET.


    def post(self, request):
        if not request.data:    # if nothing is provided in username and password.
            return Response({'Error': "Please provide username/password"}, status="400")
        # used Rest Requests request.data insted of request.POST , can be compatible with POST,PUT etc
        username = request.data['username']     # gets the username
        password = request.data['password']     # gets the password
        try:
            user = User.objects.get(username=username, password=password)   # Checks for Valid username and password.
        except User.DoesNotExist:
            return Response({'Error': "Invalid username or password"}, status="400")
        if user:
                payload = {
                    'username': user.username,
                    'password': user.password,
                }
                jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256')}
                # generates the token using payload information.
                # print(jwt_token)
                template = env.get_template('dashboard.html')   # using Jinja2 to get the dashboard template
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
        else:
            return Response(
                json.dumps(list({'Error': "Invalid credentials"})),
                status=400,
                content_type="application/json"
            )
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



