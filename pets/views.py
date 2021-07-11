from django.shortcuts import render
from .models import Pet, Follow

def newpet(request):
    return render(request, 'pets/newpet.html')

def showpet(request):
    if request.method == 'GET': 
      pet = Pet.objects.get(id=id)
      return render(request, 'pets/showpet.html', {'pet':pet})
    elif request.method == 'POST': 
        name = request.POST['name']
        image = request.POST ['image']
        introduction = request.POST['introduction']
        pet = Pet.objects.create(name=name, image=image, introduction=introduction, owner=request.user)
        return render(request, 'pets/showpet.html', {'pet':pet})

def deletepet(request):
  pass
def updatepet(request):
  pass