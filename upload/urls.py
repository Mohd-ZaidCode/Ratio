from django.urls import path
from . import views

urlpatterns = [
    # URL for the video upload form
    path('upload/', views.upload_video, name='upload_video'),
    path('videos/', views.video_list, name='video_list'),
    path('videos/delete/', views.delete_video, name='delete_video'),
]