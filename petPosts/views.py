from django.shortcuts import render, redirect
from .models import Post, Photo, Comment, Like, CommentLike
from accounts.models import Profile
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def index(request):
    if request.method == 'GET': 
        posts = Post.objects.all().order_by('-created_at')
        return render(
            request, 
            'petPosts/index.html', 
            {
                'posts': posts, 
            }
        )
    elif request.method == 'POST': 
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(title=title, content=content, author=request.user)
        for img in request.FILES.getlist('imgs'):
            photo = Photo()
            photo.post = post
            photo.image = img
            photo.save()
        return redirect('petPosts:index') 

def ranking(request):
    posts_by_ranking=Posts.objects.annotate(count=Count('like_users')).order_by('count')
    return render (request, 'posts/index.html', {'post_rank':posts_by_ranking})

def followinglist(request):
    followings = request.user.followings.all()
def list(request):
    
    my_posts = request.user.post_set.all()
    # 내가 팔로잉 하는 사람들
    followings = request.user.following_pets.all()
    #내 계정이 팔로우하고 있는 pet들의 post or 내 포스팅
    posts = Post.objects.filter(Q(pet__in=request.user.profile.following_pets.all())|Q(pet=request.user.profile.pet_set)).order_by('-id')
    comment_form = CommentForm()
    return render(request, 'posts/index.html', {'posts':posts, 'comment_form':comment_form})

def new(request):
    return render(request, 'petPosts/new.html')


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
        post.first().tags.set(request.POST.getlist('tags'))

        return redirect('petPosts:show', id=id)


class CommentView:
    def create(request, id):
        content = request.POST['content']
        comment = Comment.objects.create(post_id=id, content=content, author=request.user)
        current_time = comment.created_at.strftime('%Y년 %m월 %d일 %-H:%M')

        post = Post.objects.get(id=id)
        return JsonResponse({
            'commentId': comment.id,
            'commentCount': post.comment_set.count(),
            'commentLikeCount': comment.like_users.count(), 
            'createdTime': current_time,
            'author': request.user.username 
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
