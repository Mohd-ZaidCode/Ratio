from django.http import HttpResponse
from django.shortcuts import redirect, render


from .forms import VideoForm
from .models import Video

# Create your views here.
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})

def video_list(request):
    videos = Video.objects.all()
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        video = Video.objects.get(id=video_id)
        video.delete()
        return redirect('video_list')
    context = {'videos': videos}
    if len(videos) == 0:
        return redirect('/upload')
    return render(request, 'video_list.html', context)


# def delete_video(request):
#     if request.method == 'POST':
#         video_id = request.POST.get('video_id')
#         video = Video.objects.get(id=video_id)
#         video.delete()
#     return redirect('video_list')