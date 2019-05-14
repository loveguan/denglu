"""denglu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls import re_path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('test/',views.test),
    re_path('index/',views.index),
    re_path('login/',views.login),
    re_path('register/',views.register),
    re_path('logout/',views.logout),
    re_path(r'^check_code/$', views.check_code),
    re_path(r'^confirm/$', views.user_confirm),
    re_path(r'^send_msg/$', views.send_msg),
    path('',views.index)
]
