from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django import forms
from accounts.models import Profile


class Pet(models.Model):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
  name = models.CharField(max_length=20, blank=True)
  PET_CHOICES = (
      ('p1', '강아지'),
      ('p2', '고양이'),
      ('p3', '햄스터'),
      ('p4', '포유류'),
      ('p5', '조류'),
      ('p6', '어류'),
      ('p7', '파충류'),
      ('p8', '거미/전갈')
  )
  category = models.CharField(max_length=2, choices=PET_CHOICES, blank=True, null=True, verbose_name="category")
  #age?
  introduction = models.CharField(max_length=100, blank=True)
  image = models.ImageField(upload_to='images/',blank=True, null=True)
  follow_users = models.ManyToManyField(User, blank=True, related_name='following_pets', through='Follow')

  def __str__(self):     
    return f'id={self.id}, name={self.name}'

class PetForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(PetForm, self).__init__(*args, **kargs)

    class Meta:
         model = Pet
         fields = '__all__'

class Follow(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
