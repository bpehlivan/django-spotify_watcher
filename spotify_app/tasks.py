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

    user = User.objects.get(username='enivecivokke')
    social = user.social_auth.get(provider='spotify')
    token = social.extra_data['access_token']
    ref_token = social.extra_data['access_token']
    spotify_wrapper = SpotifyApi(token,ref_token)
    spotify_wrapper.get_playlists()
