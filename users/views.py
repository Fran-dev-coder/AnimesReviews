from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile, Follow
from reviews.utils import get_user_profile
from reviews.models import Review, Anime
# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exit')

        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Incorrect password ')

    return render(request, 'users/login-register.html')

def logoutUser(request):
    logout(request)
    messages.success(request,'User was logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, f"Welcome, {user.first_name}, to AnimeReview")
            login(request, user)
            return redirect('settings')
        else:
            messages.error(request,'An error has occurred during registration')

    context = {'page':page,'form':form}
    return render(request,'users/login-register.html', context)

def profile(request,id):
    profile = get_object_or_404(Profile,id=id)
    profile_login = get_user_profile(request.user)
    reviews = Review.objects.filter(owner=profile).order_by('-created_at')
    
    if request.method == 'POST':
        if profile_login:
            if 'follow' in request.POST:
                Follow.objects.create(follower=profile_login, following=profile)
            elif 'unfollow' in request.POST:
                Follow.objects.filter(follower=profile_login, following=profile).delete()
    
    is_following =  Follow.objects.filter(follower=profile_login, following=profile).exists() if profile_login else False

    context = {'profile':profile,'user':profile.user,'reviews':reviews,'is_following':is_following}
    return render(request,'users/profile.html',context)

@login_required(login_url='login')
def profileSettings(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile saved')
            return redirect('settings')

    context = {'form':form}
    return render(request,'users/settings.html',context)

def explore(request):
    profile = get_user_profile(request.user)
    if profile:
        following_profile = profile.following.values_list('following',flat=True)
        followed_reviews = Review.objects.filter(owner__in=following_profile).exclude(owner=profile)
        other_reviews = Review.objects.exclude(owner__in=following_profile).exclude(owner=profile)
    else:
        followed_reviews = []
        other_reviews = Review.objects.all()

    context = {'profile':profile,'followed_reviews':followed_reviews,'other_reviews':other_reviews}
    return render(request,'users/explore.html',context)