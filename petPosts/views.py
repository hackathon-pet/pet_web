from django.shortcuts import render, redirect
from .models import Post, Comment, Like, CommentLike
from accounts.models import Profile
from django.db.models import Count
from django.contrib.auth.models import User
from tags.models import Tag
from django.http import JsonResponse

# Create your views here.
def index(request):
    if request.method == 'GET': 
        posts = Post.objects.all().order_by('-created_at')
        tags = Tag.objects.all()
        colleges = Profile.objects.exclude(college="").values('college').annotate(count=Count('college')).order_by('count')
        users_with_same_college = None
        users_with_same_major = None
        
        if request.user.is_authenticated:
            if (request.user.profile.college != ""):
                users_with_same_college = User.objects.filter(profile__college=request.user.profile.college).exclude(id=request.user.id)
            if (request.user.profile.major != ""):
                users_with_same_major = User.objects.filter(profile__major=request.user.profile.major).exclude(id=request.user.id)
            
        return render(
            request, 
            'petPosts/index.html', 
            {
                'posts': posts, 
                'colleges': colleges, 
                'users_with_same_college': users_with_same_college, 
                'users_with_same_major': users_with_same_major,
                'tags': tags
            }
        )
    
    elif request.method == 'POST': 
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(title=title, content=content, author=request.user)
        post.tags.set(request.POST.getlist('tags'))
        return redirect('petPosts:index') 


def new(request):
    tags = Tag.objects.all()
    return render(request, 'petPosts/new.html', {'tags': tags})


def show(request, id):
    post = Post.objects.get(id=id)
    tags = Tag.objects.filter(posts=post)
    return render(request, 'petPosts/show.html', {'post':post, 'tags': tags})


def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete() 
    if request.method == 'DELETE' : 
        return JsonResponse({'postLikeCount': request.user.like_posts.count()});
    
    return redirect('petPosts:index') 

def update(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        tags = Tag.objects.all()
        return render(request, 'petPosts/update.html', {'post':post, 'tags': tags})
    
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