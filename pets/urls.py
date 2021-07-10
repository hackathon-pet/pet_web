from django.urls import path
from pets import views

app_name = 'pets'
urlpatterns = [
    path('newpet/', views.newpet, name='newpet'),
    path('<int:id>/', views.showpet, name='showpet'),
    path('<int:id>/deletepet/', views.deletepet, name='deletepet'),
    path('<int:id>/updatepet/', views.updatepet, name='updatepet'),
]

