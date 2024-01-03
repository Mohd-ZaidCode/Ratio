from django.contrib import admin
from django.urls import path, include
from .  import views
from authentication import views as authview
from authentication.views import logout





app_name = 'search'


urlpatterns = [

    path('',views.index,name='index'),
     
    
    
]