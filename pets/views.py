from django.shortcuts import render, redirect
from .models import Pet, PetForm, Follow
from django.http import JsonResponse

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

def showpet(request):
  pet = Pet.objects.get(id=id)
  return render(request, 'pets/showpet.html', {'pet':pet})

def deletepet(request):
  pass
def updatepet(request):
  pass

class FollowView:
    def create(request, id):
        pet = Pet.objects.get(id=id)
        follow_status = pet.follower_users.filter(user_id=request.user.id)
        if follow_status.count() > 0:
            pet.follower_users.get(user=request.user).delete()
        else:
            Follow.objects.create(user=request.user, pet=pet)
        return JsonResponse({
            'followStatus': follow_status.count(), 
            'petFollowCount': pet.like_set.count(), 
            'userFollowCount': request.user.follow_pet.count()
        })