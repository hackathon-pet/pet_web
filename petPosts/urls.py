from django.urls import path
from petPosts import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'petPosts'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('<int:id>/new/', views.new, name='new'),
    path('<int:id>/', views.show, name='show'),
    path('<int:id>/delete/', views.delete, name='delete'), 
    path('<int:id>/update/', views.update, name='update'),
    path('<int:id>/comments/', views.CommentView.create, name='comment_create'),
    path('<int:id>/comments/<int:cid>/', views.CommentView.delete, name='comment_delete'),
    path('<int:id>/like/', views.LikeView.create, name='like'),
    path('<int:cid>/commentlike/', views.CommentLikeView.create, name='commentlike'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)