from django.shortcuts import render
from .models import Pet, PetForm, Follow

def newpet(request):
  if request.method == 'GET': 
    form = PetForm()
    return render(request, 'pets/newpet.html', {'form': form})
  elif request.method == 'POST': 
    name = request.POST['name']
    category = request.POST['category']
    image = request.POST['image']
    introduction = request.POST['introduction']
    pet = Pet.objects.create(name=name, image=image, introduction=introduction, owner=request.user, category = category)
    return render(request, 'accounts/myinfo.html', {'pet':pet})

def showpet(request):
  pet = Pet.objects.get(id=id)
  return render(request, 'pets/showpet.html', {'pet':pet})

def deletepet(request):
  pass
def updatepet(request):
  pass
