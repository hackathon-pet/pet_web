from django.shortcuts import render
from django.contrib.auth.models import User  
from django.contrib import auth  
from django.shortcuts import redirect 
from .models import Profile
from pets.models import Pet, Follow

def signup(request):
  if request.method == 'POST':
      if request.POST['password1'] == request.POST['password2']:
          user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
          auth.login(request, user)
          Profile.objects.filter(user=request.user).update(email=request.POST['email'], introduction=request.POST['introduction'])
          return redirect('/posts')

  return render(request, 'accounts/signup.html')

def myinfo(request):
  if request.method == 'GET':
    profile = Profile.objects.get(user=request.user)
    pets = Pet.objects.filter(owner=request.user.profile)


  return render(request, 'accounts/myinfo.html', {'pets':pets, 'profile':profile })      

def editmyinfo(request):
    if request.method == 'POST':
        Profile.objects.filter(user=request.user).update(college=request.POST['college'], major=request.POST['major'])
        return redirect('/posts')

    return render(request, 'accounts/editmyinfo.html')

