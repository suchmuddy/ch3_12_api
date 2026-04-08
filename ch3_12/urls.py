"""
URL configuration for ch3_12 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search_list/',views.search_list,name='search_list'),#name,AI常用,目的是幫這個網址取一個代號,django不再靠網址字串連接(/search_list/)
    path('search_name/',views.search_name,name='search_name'),
    path('index/',views.index,name='index'),
    path('post/',views.post,name='post'),
    path('edit/<int:id>/',views.edit,name='edit'),
    path('delete/<int:id>/',views.delete,name='delete'),
    #web api
    path('getAllItems/',views.getAllItems,name='getAllItems'),
    path('getItem/<int:id>/',views.getItem,name='getItem'),

]

