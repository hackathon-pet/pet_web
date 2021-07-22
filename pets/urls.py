from django.urls import path
from pets import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pets'
urlpatterns = [
    path('newpet/', views.newpet, name='newpet'),
    path('<int:id>/', views.showpet, name='showpet'),
    path('<int:id>/deletepet/', views.deletepet, name='deletepet'),
    path('<int:id>/updatepet/', views.updatepet, name='updatepet'),
    path('<int:id>/follow/', views.FollowView.create, name='follow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)