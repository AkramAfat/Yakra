from django.shortcuts import render,redirect
from .models import Profile,Tweet
from django.contrib import messages
from .forms import TweetForm,SignUpForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
 if request.user.is_authenticated:
    form = TweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
                tweet =form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request,("Your Tweet has been posted "))
                return redirect('home')
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request,'home.html',{"tweets":tweets, "form":form})
 else:
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
    


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You Have Been Logged In "))
            return redirect('home')
        else:
             messages.success(request,("Password Invalid Please Try Again "))
             return redirect('login')


    else:   
        return render(request,"login.html",{})



def logout_user(request):
    logout(request)
    messages.success(request,("You Have Been Logged Out | Login To Tweet "))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #first_name = form.cleaned_data['last_name']
            #first_name = form.cleaned_data['email']
            #login user
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,("Welcome To Yakra U have Successfully Join Us"))
            return redirect('home')

    return render(request,"register.html",{'form':form})


def update_user(request):   
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = SignUpForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request,current_user)
            messages.success(request,("Your Profile Has Been Updated"))
            return redirect('home')
        return render(request,"update_user.html",{'form':form})

    else:
        messages.success(request,("You Must Login to Update Your Profile"))
        return redirect('home')

