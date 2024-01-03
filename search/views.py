
from django.shortcuts import render,redirect
from django.urls import reverse
from isodate import parse_duration
from django.conf import settings
import requests
from authentication.views import home


# def redi(request):
#     if request.POST['submit']=='random':
#         url = reverse('authentication:sVideo')
#         return redirect(url)




def index (request):
    videos = []
    

    if request.method =='POST' :
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 27 ,
            'type':'video'

        }
        
        r= requests.get(search_url,params=search_params)
        results= r.json()['items']
        video_ids=[]
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit']=='random':
            return redirect(f'https://www.youtube.com/watch?v=MkcfB7S4fq0&ab_channel=ApnaCollege')
        

        
    

        video_params ={

            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet, contentDetails',
            'maxResults' : 27,
            'id' : ','.join(video_ids)

        }

        r=requests.get(video_url, params = video_params )

        results= r.json()['items']


        for result in results:
            
            video_data = {
                'title' :  result['snippet']['title'],
                'id' : result['id'],
                'url':f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)

    
    Context = {
        'videos' : videos

    }
    
    return render(request,'search/index.html', Context)
