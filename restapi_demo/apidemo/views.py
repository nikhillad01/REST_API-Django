from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import stock,Registration
from .serializers import stockSerializer
from .forms import Registrationform
from django.contrib.auth import get_user_model
import jwt,json
from rest_framework.response import Response
from .serializers import TokenAuthentication
from .serializers import registrationSerializer
from rest_framework.generics import CreateAPIView




def index(request):
    return render(request, 'index.html', {})

# /stocks
class StockList(APIView):


    def get(self,request):
        stocks=stock.objects.all()
        serializer = stockSerializer(stocks)

        return Response(serializer.data)


    def post(self):
        pass

def register(request):              # Normal Registration without Rest Framework.
    form = Registrationform(request.POST or None)
    if form.is_valid():
        form.save()
    context ={
        'form':form
    }
      # if request.method == 'POST':
      #      add_to_database = Registration()
      #      add_to_database.uname = request.POST.get('uname')
      #      add_to_database.pwd = request.POST.get('pass')
      #      add_to_database.cpass = request.POST.get('cpass')
      #      add_to_database.save()

           #return HttpResponse('<h1> Successfully registered</h1>')
    return render(request, 'registration.html',context)
           # else:
        #     return render(request, 'posts/create.html')


from .models import RestRegistration
User= get_user_model()

class UserCreateAPI(CreateAPIView):             # Registration using Rest framework Using User Model.

    serializer_class=registrationSerializer
    queryset = User.objects.all()          # fields according to User   (adds data to USER model)
    #queryset = RestRegistration.objects.all()   # # fields according to RestRegistration model.
                                                # (adds data to RestRegistration Model.)
    #registrationSerializer



class LoginView(APIView):
    serializer_class = TokenAuthentication
    queryset = User.objects.all()
    http_method_names = ['post','get']      # to use POST method by default it was using GET.




    # def post(self,request):
    #     serializer=loginSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)  #if validation is wrong or any exception occurs then it will return to user
    #     user = serializer.user
    #     if user==True:
    #         payload = {
    #             'username': user.username,
    #             'password': user.password,
    #         }
    #
    #         jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
    #         return HttpResponse(
    #             json.dumps(jwt_token),
    #             status=200,
    #             content_type="application/json"
    #         )
    #     else:
    #         return Response(
    #             json.dumps({'Error': "Invalid credentials"}),
    #             status=400,
    #             content_type="application/json"
    #         )


    # status 400= Bad Request:indicates that the server could not understand the
    # request due to invalid syntax.
    def post(self, request):
        if not request.data:    # if nothing is provided in username and password.
            return Response({'Error': "Please provide username/password"}, status="400")

        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username, password=password)
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