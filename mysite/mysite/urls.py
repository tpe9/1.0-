"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from django.conf.urls import include
 
from . import views
 
urlpatterns = [
	path('admin/', admin.site.urls),
	#url(r'^$', views.hello),
	url(r'^index/', views.index),
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^forget/', views.forget),
    url(r'^reset_pd/', views.reset_pd),
    url(r'^logout/', views.logout),
    url(r'^hello/', views.hello),
    url(r'^get_vcode/', views.get_vcode),
    url(r'^myinformation_edit/', views.myinformation_edit),
    url(r'^create_pro/', views.create_pro),
    url(r'^project_enter/', views.project_enter),
    url(r'^project_inf/', views.project_inf),
    url(r'^check_in/', views.check_in),
    url(r'^my_project/', views.my_project),
    url(r'^business_apply/', views.business_apply),
    url(r'^ask_for_leave/', views.ask_for_leave),
    url(r'^check_out/', views.check_out),
]