"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
import petPosts.views
import pets.views
import accounts.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', petPosts.views.index), 
    path('posts/', include('petPosts.urls')),
    path('pets/', include('pets.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', accounts.views.signup, name='signup'),
    path('accounts/myinfo/', accounts.views.myinfo, name='myinfo'),
    path('accounts/editmyinfo/', accounts.views.editmyinfo, name='editmyinfo'),
    path('social_accounts/', include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
