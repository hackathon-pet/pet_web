from django.shortcuts import render, redirect
from .models import Post, Photo, Comment, Like, CommentLike
from pets.models import Pet,PetForm
from accounts.models import Profile
from pets.models import Pet
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.http import JsonResponse
from pets.models import Pet
from django import forms
from collections import defaultdict
import json
from json import JSONEncoder
import locale
# Create your views here.

def index(request):

    if request.method == 'GET': 
        pets_by_ranking=[]
        categories={}
        form = PetForm()
        category=set()
        for x,y in form.fields['category'].choices:
            if x!='':
                category.add(y)
                categories[y]={}
                category_pet=Pet.objects.filter(category=x)
                pet_by_category=[]
                for pet in category_pet:
                    sumall=0
                    for post in pet.post_set.all():
                        p = Post.objects.filter(id=post.id).annotate(num_like=Count('like_users'))
                        sumall+=(p[0].num_like)
                    pet_by_category.append([pet, sumall])
                pet_by_category.sort(key=lambda x: -x[1])
                categories[y]=pet_by_category
        for pet in Pet.objects.all():
            sum_of_like=0
            for post in pet.post_set.all():
                p = Post.objects.filter(id=post.id).annotate(num_like=Count('like_users'))
                sum_of_like+=(p[0].num_like)
            pets_by_ranking.append([pet, pet.name, sum_of_like, pet.image])
        pets_by_ranking.sort(key=lambda x: -x[2])
        if request.user.is_authenticated:
            feed = Post.objects.filter(pet__in=request.user.following_pets.all()).order_by('-created_at')
            following_pet=request.user.following_pets.all()
            return render(
                request, 
                'petPosts/index.html', 
                {
                    'pet_rank':pets_by_ranking,
                    'feed': feed,
                    'following_pets':following_pet,
                    'categories': categories
                }
            )
        else:
            feed=Post.objects.all().order_by('-created_at')
            return render(
                request, 
                'petPosts/index.html', 
                {
                    'pet_rank':pets_by_ranking,
                    'feed': feed,
                    'categories': categories
                }
            )


def new(request, id):
    if request.method == 'GET':
        pet = Pet.objects.get(id=id)
        id = pet.id
        return render(request, 'petPosts/new.html', {'pet':pet, 'id':id})

    elif request.method == 'POST': 
        title = request.POST['title']
        content = request.POST['content']
        pet = Pet.objects.get(id=id)
        post = Post.objects.create(title=title, content=content, pet=pet)
        post.save()
        for img in request.FILES.getlist('imgs'):
            photo = Photo()
            photo.post = post
            photo.image = img
            photo.save()
        return redirect('pets:showpet', id=id)


def show(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'petPosts/show.html', {'post':post})


def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete() 
    if request.method == 'DELETE' : 
        return JsonResponse({'postLikeCount': request.user.like_posts.count()})
    
    return redirect('petPosts:index') 

def update(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        return render(request, 'petPosts/update.html', {'post':post})
    
    elif request.method == 'POST':
        post = Post.objects.filter(id=id)
        post.update(title=request.POST['title'], content=request.POST['content'])

        return redirect('petPosts:show', id=id)


class CommentView:
    def create(request, id):
        content = request.POST['content']
        comment = Comment.objects.create(post_id=id, content=content, author=request.user)
        current_time = comment.created_at.strftime("%Y년 %m월 %d일".encode('unicode-escape').decode()).encode().decode('unicode-escape')
        
        post = Post.objects.get(id=id)
        return JsonResponse({
            'commentId': comment.id,
            'commentCount': post.comment_set.count(),
            'commentLikeCount': comment.like_users.count(), 
            'createdTime': current_time,
            'author':request.user.username
        })
        
    def delete(request, id, cid):
        comment = Comment.objects.get(id=cid)
        comment.delete()
        post = Post.objects.get(id=id)
        return JsonResponse({'commentCount': post.comment_set.count()})

class LikeView:
    def create(request, id):
        post = Post.objects.get(id=id)
        like_list = post.like_set.filter(user_id=request.user.id)
        if like_list.count() > 0:
            post.like_set.get(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, post=post)
        return JsonResponse({
            'postLikeOfUser': like_list.count(), 
            'postLikeCount': post.like_set.count(), 
            'userLikeCount': request.user.like_posts.count()
        })

class CommentLikeView:
    def create(request, cid):
        comment = Comment.objects.get(id=cid)
        like_list = comment.commentlike_set.filter(user_id=request.user.id)
        if like_list.count() > 0:
            comment.commentlike_set.get(user=request.user).delete()
        else:
            CommentLike.objects.create(user=request.user, comment=comment)
        return JsonResponse({'commentLikeCount': comment.commentlike_set.count()})
