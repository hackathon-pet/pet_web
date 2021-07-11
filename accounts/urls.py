from django.urls import path
from accounts import views

urlpatterns = [    
    path('signup/', views.signup, name='signup'),
    path('<int:id>/myinfo/', views.myinfo, name='myinfo'),
    path('<int:id>/editmyinfo/', views.editmyinfo, name='editmyinfo'),
]