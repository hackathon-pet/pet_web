from django.shortcuts import render
from .models import Pet, Follow

def new(request):
    return render(request, 'pets/new.html')

def show(request):
    if request.method == 'GET': 
      pet = Pet.objects.get(id=id)
      return render(request, 'pets/show.html', {'pet':pet})
    elif request.method == 'POST': 
        name = request.POST['name']
        image = request.POST ['image']
        introduction = request.POST['introduction']
        pet = Pet.objects.create(name=name, image=image, introduction=introduction, owner=request.user)
        return render(request, 'pets/show.html', {'pet':pet})
