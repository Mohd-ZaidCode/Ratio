from email.message import EmailMessage
from django.template.loader import render_to_string
from base64 import urlsafe_b64decode, urlsafe_b64encode
from Ratio import settings
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage,send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from . tokens import generate_token
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

# Create your views here.



def home(request):
    return render(request,"authentication/index.html")


def signup(request):
    
    if request.method =="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username is Alredy taken! Please try other username!")
            return redirect('home')
        

        # if User.objects.filter(email=email):
        #     messages.error(request, "Email is already registered!")
        #     return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username can't be greater then 10 character!")
           
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
           
        if not username.isalnum():
            messages.error(request, "password should be alphanumeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email ,pass1)
        myuser.first_name =fname
        myuser.last_name =lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your Account is succesfully created.We have sended you a confirmation mail please confirm your email address")
        

        #!------Welcome email-------!


        subject="Welcome to RATIO!!- Greets from Zaid,Tanya and Ishan "
        message = "Hello, "+myuser.first_name+" "+myuser.last_name+"!!\nits nice to see you exploring our Educational Comunity Ratio \nWe Have Also Sent You an email to confirm\n \n Thank You!!!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message,from_email, to_list,fail_silently=True)



        #!------Confirmation mail--------!

        current_site = get_current_site(request)
        email_subject ="Confirm Your Email --Ratio Leraning"
      
        message2=render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email=EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],)
        email.fail_silently = True
        email.send()

        


        return redirect('signin')

    return render(request,"authentication/signup.html") 
    

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user =  authenticate(username=username,password=pass1)

        if user is not None:
            login(request, user)
            fname=user.first_name
            return render(request, "authentication/index.html", {'fname':fname})
        else:
            messages.error(request, "Bad Credentials! Please try again")
            return redirect('home')

    return render(request,"authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Succesfully!")
    return redirect('home')

def activate (request,uidb64,token ):
    try:
        uid =force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except (TypeError, ValueError,OverflowError,User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return redirect(request, 'activation_failed.html')
    

