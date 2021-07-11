from django.shortcuts import render, redirect
from .models import Pet, PetForm, Follow
from django.http import JsonResponse

def newpet(request, id):
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

def deletepet(request):
  pass
def updatepet(request):
  pass

class FollowView:
  def create(request, id):
    pet = Pet.objects.get(id=id)
    follow_status = pet.follow_users.filter(id=request.user.id)
    if follow_status.count() > 0:
      pet.follow_users.get(id=request.user.id).delete()
    else:
      Follow.objects.create(user=request.user, pet=pet)
    return JsonResponse({
        'followStatus': follow_status.count(), 
        'petFollowCount': pet.follow_set.count(), 
        'userFollowCount': request.user.following_pet.count()
      })