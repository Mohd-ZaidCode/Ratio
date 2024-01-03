from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='videos/')
    caption = models.TextField(default=" ")
    uploaded_at = models.DateTimeField(auto_now_add=True)