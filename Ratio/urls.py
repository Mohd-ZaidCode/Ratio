"""Ratio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from upload import views as uviews
import apps.public.views, apps.chat.views



urlpatterns = [
    path('Ratioapp/', include('Ratioapp.urls')),
    path('admin/', admin.site.urls),
    path('',include('authentication.urls')),
    path('searchVideo',include('search.urls')),
     # URL for the video upload form
    path('upload/', uviews.upload_video, name='upload_video'),

    # URL for the video list page
    path('videos/', uviews.video_list, name='video_list'),
    path('chatapp', apps.public.views.index_page),
    path('profile', apps.public.views.profile, name='profile'),
    re_path(r'^login', apps.public.views.login_view, name='login'),
    path('register', apps.public.views.register_view, name='register'),
    path('profile/my-room', apps.public.views.my_room, name='my_room'),
    path('profile/room/<str:room_code>/setting', apps.public.views.room_settings, name='room_settings'),
    path('chat/', include('apps.chat.urls'), name='chat'),
    path('api/user/', include('apps.public.api_urls')),
    path('api/chat/', include('apps.chat.api_urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)