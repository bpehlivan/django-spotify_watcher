from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .spotify_api import SpotifyRefreshUsers,SpotifyApi
from django.contrib.auth.models import User
@shared_task
def add():
    print('test')
    return True


@shared_task
def call_refresh_token():
    spotify=SpotifyRefreshUsers()
    spotify.refresh_token()

@shared_task
def get_songs():

    users = User.objects.all()
    for user_object in users:
        try:
            social = user_object.social_auth.get(provider='spotify')
            spotify_wrapper = SpotifyApi(social)
            spotify_wrapper.get_currently_playing()
        except:
            pass
