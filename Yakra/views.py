from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Profile
from django.contrib import messages
from .models import Tweet

def home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by("-created_at")
    return render(request,'home.html',{"tweets":tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request,'profile_list.html',{"profiles":profiles})
    else:
        messages.success(request,("You Must Be logged In to Enter this Page"))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")
        #post form logic :
        if request.method == "POST":
            #get current user
            current_user_profile = request.user.profile
            #Get form data
            action = request.POST['follow']
            #Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
                #save the profile 
                current_user_profile.save()



        return render(request,"profile.html",{"profile":profile, "tweets":tweets})
    else:
         messages.success(request,("You Must Be logged In to Enter this Page"))
         return redirect('home')