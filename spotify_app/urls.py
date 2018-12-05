
from django.urls import path, include
from . import views

app_name='spotify_app'


urlpatterns = [
    path('weekly_chart/', views.weekly_chart,name='weekly_chart'),
    path('recommended_songs/', views.recommended_songs,name='recommended_songs'),
]
