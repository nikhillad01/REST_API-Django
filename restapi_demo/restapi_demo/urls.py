"""restapi_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
#from restapi_demo.apidemo import views
from apidemo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('stocks/', views.StockList.as_view(),name='stocks'),
    path('register/', views.register,name='register'),
    path('rest_register/', views.UserCreateAPI.as_view(),name='rest_register'),
    path('rest_login/', views.LoginView.as_view(),name='rest_login'),
    #path('confirm/',views.register_with_confirm_password.as_view(),name='confirm')
    path('rest_logout/',views.LogoutView.as_view()),
    path('dash/',views.dash),
    #path('rest-auth/', include('rest_auth.urls')),
    #path('rest-auth/registration/', include('rest_auth.registration.urls')),
]#UserCreateAPI
#urlpatterns = format_suffix_patterns(urlpatterns)