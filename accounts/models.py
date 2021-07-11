from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)    
  #after making 'category' : like_category
  email = models.CharField(max_length=30, blank=True)    
  introduction = models.CharField(max_length=100, blank=True)

  def __str__(self):   # 추가        
    return f'id={self.id}, user_id={self.user.id}'

  @receiver(post_save, sender=User)  
  def create_user_profile(sender, instance, created, **kwargs):        
    if created:          
      Profile.objects.create(user=instance)  
  
  @receiver(post_save, sender=User)  
  def save_user_profile(sender, instance, **kwargs):        
    instance.profile.save()

