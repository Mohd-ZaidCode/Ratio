from . import views
from django.contrib import admin
from django.urls import path, include
from search import views as secview
from search.views import index

urlpatterns = [
   path('', views.home,name="home"),
   path('signup',views.signup,name="signup"),
   path('signin',views.signin,name="signin"),
   path('signout',views.signout,name="signout"),
   path('searchV',secview.index,name="searchV"),


   path('activate;<uidb64>/<token>',views.activate,name="activate"),

]
