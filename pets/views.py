from django.shortcuts import render, redirect
from .models import Pet, PetForm, Follow
from django.db.models import Count
from django.http import JsonResponse
from django.http import HttpResponseRedirect

def newpet(request):
  if request.method == 'GET': 
    form = PetForm()
    return render(request, 'pets/newpet.html', {'form': form})
  elif request.method == 'POST': 
    name = request.POST['name']
    category = request.POST['category']
    image = request.FILES['image']
    introduction = request.POST['introduction']
    owner=request.user.profile
    pet = Pet.objects.create(name=name, image=image, introduction=introduction, owner=owner, category = category)
    return redirect('/accounts/myinfo')

def showpet(request, id):
  pet = Pet.objects.get(id=id)
  return render(request, 'pets/showpet.html', {'pet':pet})

def deletepet(request, id):
  pet = Pet.objects.get(id=id)
  pet.delete()
  return redirect('/accounts/myinfo')

def updatepet(request, id):
  if request.method == 'GET':
    pet = Pet.objects.get(id=id)
    form = PetForm()
    return render(request, 'pets/updatepet.html', {'pet':pet, 'form': form})
  elif request.method == 'POST':
    pet = Pet.objects.filter(id=id)
    name = request.POST['name']
    category = request.POST['category']
    image = request.FILES['image']
    introduction = request.POST['introduction']
    owner=request.user.profile
    pet.update(name=name, image=image, introduction=introduction, owner=owner, category = category)
    return redirect('pets:showpet', id=id)

class FollowView:
  def create(request, id):
    pet = Pet.objects.get(id=id)
    follow_status = pet.follow_users.filter(id=request.user.id)
    if follow_status.count() > 0:
      pet.follow_set.get(user=request.user.id).delete()
    else:
      Follow.objects.create(user=request.user, pet=pet)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
