from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from accounts.models import Profile

# Create your models here.
class Pet(models.Model):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
  name = models.CharField(max_length=20, blank=True)
  introduction = models.CharField(max_length=100, blank=True)
  image = models.ImageField(upload_to='images/',blank=True, null=True)
  follow_users = models.ManyToManyField(User, blank=True, related_name='like_pets', through='Follow')

  def __str__(self):     
    return f'id={self.id}, name={self.name}'

class Follow(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
