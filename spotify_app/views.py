from django.shortcuts import render
import pprint
import sys

import spotipy
import spotipy.util as util
import json
import requests
from django.contrib.auth.models import User
from .spotify_api import SpotifyApi,SpotifyRefreshUsers


def weekly_chart(request):
    if request.user.is_authenticated:
        print('USER ACCESS')
        print(request.user)
    else:
        print('USER CANT ACCESS')
        print(request.user)
    return render(request, 'weekly_chart.html')


def recommended_songs(request):
    user = User.objects.get(username='enivecivokke')
    social = user.social_auth.get(provider='spotify')
    token = social.extra_data['access_token']
    ref_token = social.extra_data['access_token']
    spotify_wrapper = SpotifyApi(token,ref_token)
    spotify_wrapper.get_playlists()
    #print(request.user)
    #user = User.objects.get(username=request.user)
    #print(user)
    #social = user.social_auth.get(provider='spotify')
    #token = social.extra_data['access_token']
    #print(token)
    #spotify=spotify_api(token,refresh_token)
    '''
    user = User.objects.get(id=1)
    social = user.social_auth.get(provider='spotify')
    token=social.extra_data['access_token']
    '''

    return render(request, 'recommended_songs.html')