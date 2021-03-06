from django.shortcuts import render, redirect
from .models import Pet, PetForm, Follow, Petimage
from petPosts.models import Post
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
    introduction = request.POST['introduction']
    owner=request.user.profile
    pet = Pet.objects.create(name=name, introduction=introduction, owner=owner, category = category)
    pet.save()
    petImage = Petimage()
    petImage.pet = pet
    petImage.image = request.FILES['image']
    petImage.save()
    return redirect('/accounts/myinfo')

def showpet(request, id):
  pet = Pet.objects.get(id=id)
  posts = Post.objects.filter(pet=pet)
  return render(request, 'pets/showpet.html', {'pet':pet, 'posts':posts})

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
    pet_ = Pet.objects.get(id=id)
    Petimage.objects.filter(pet=pet_).delete()
    petImage = Petimage()
    petImage.pet = pet_
    petImage.image = request.FILES['image']
    petImage.save()
    name = request.POST['name']
    category = request.POST['category']
    introduction = request.POST['introduction']
    owner=request.user.profile
    pet.update(name=name, introduction=introduction, owner=owner, category = category)
    return redirect('pets:showpet', id=id)

class FollowView:
  def create(request, id):
    pet = Pet.objects.get(id=id)
    follow_status = pet.follow_users.filter(id=request.user.id)
    if follow_status.count() > 0:
      pet.follow_set.get(user=request.user.id).delete()
    else:
      Follow.objects.create(user=request.user, pet=pet)
    follow=Follow.objects.filter(pet=pet)
    return JsonResponse(  {'follow_count': follow.count()} )
