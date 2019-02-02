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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
#from restapi_demo.apidemo import views
from apidemo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('rest_register/', views.Signup,name='rest_register'),  # Registration using REST.
    path('rest_login/', views.LoginView.as_view(),name='rest_login'),       # REST Login.
    #path('confirm/',views.register_with_confirm_passwordthis is comment.as_view(),name='confirm')
    path('rest_logout/',views.LogoutView.as_view()),
    path('dash/',include('rest_framework.urls', namespace='rest_framework')),
    path('login/', views.user_login,name='login'),
    url(r'^signup/$', views.Signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
