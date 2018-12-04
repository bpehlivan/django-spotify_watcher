
from django.urls import path, include
from . import views

app_name='auth_home'


urlpatterns = [
    path('login/', views.login_page,name='login'),
    path('home/', views.home_page,name='home'),
    path('', views.home_page,name='home'),


]
