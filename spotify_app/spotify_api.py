import json
import logging
import requests
from datetime import datetime
from django.contrib.auth.models import User
import os
from .models import user_tracks_history,spotify_albums,spotify_tracks
from spotify_app.api_spotify_wrapper import Spotify
# ts = int("1284101485")
# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
import time
# create logger with 'spam_application'
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class SpotifyApi():
    def __init__(self, user_object):
        self.auth_token = user_object.extra_data['access_token']
        self.refresh_token = user_object.extra_data['access_token']
        self.user_id = user_object.user_id
        print(self.auth_token,self.user_id)

    def get_currently_playing(self):

        print(self.auth_token)
        print(self.user_id)
        url = "https://api.spotify.com/v1/me/player/currently-playing"
        payload = ""
        headers = {'Authorization': "Bearer " + self.auth_token,
                   'cache-control': "no-cache"}

        response = requests.request("GET", url, data=payload, headers=headers)

        try:
            data = response.json()
            defaults = {
                'timestamp': datetime.fromtimestamp(float(data["timestamp"]) / 1000),
                'user_id': self.user_id,
                'playlist_href': data["context"]["href"] if data["context"]["href"] else None,
                'artist_id': " ".join(artist["id"] for artist in data["item"]["album"]["artists"]),
                'album_id': data["item"]["album"]["id"] if data["item"]["album"]["id"] else None,
                'track_id': data["item"]["id"] if data["item"]["id"] else None,
                'track_name': data["item"]["name"] if data["item"]["name"] else None,
                'progress_ms': data["progress_ms"] if data["progress_ms"] else None,
                'currently_playing_type': data["currently_playing_type"] if data["currently_playing_type"] else "",
                'is_playing': data["is_playing"] if data["is_playing"] else None
            }


            obj, created = user_tracks_history.objects.update_or_create(
                timestamp=datetime.fromtimestamp(float(data["timestamp"]) / 1000),
                user_id=self.user_id, defaults=defaults
            )
            obj.save()
        except Exception as e:
            pass


    def get_user_recently_played(self):
        '''
        This is a heavy method that updates albums,tracks and user history

        :return:
        '''
        datas=Spotify(auth=self.auth_token).current_user_recently_played()

        for data in datas["items"]:
            defaults_album = {
            'album_id': data["track"]["album"]["id"] if data["track"]["album"]["id"] else None,
            'album_name': data["track"]["album"]["name"] if data["track"]["album"]["name"] else None,
            'album_uri': data["track"]["album"]["uri"] if data["track"]["album"]["uri"] else None,
            'album_artists_ids': '',
            'album_href': data["track"]["album"]["href"] if data["track"]["album"]["href"] else None,}
            obj, created = spotify_albums.objects.update_or_create(
                album_id=data["track"]["album"]["id"] if data["track"]["album"]["id"] else None,
                defaults=defaults_album
            )
            obj.save()


            defaults_tracks = {
            'track_id': data["track"]["id"] if data["track"]["id"] else None,
            'track_name': data["track"]["name"] if data["track"]["name"] else None,
            'track_popularity' : data["track"]["popularity"] if data["track"]["popularity"] else None,
            'track_duration': data["track"]["duration_ms"] if data["track"]["duration_ms"] else None,
            'track_uri': " ".join(artist["id"] for artist in data["track"]["album"]["artists"]),
            'track_artist_id': '',
            'track_href': data["track"]["album"]["href"] if data["track"]["album"]["href"] else None,
            'track_artist_name':" ".join(artist["name"] for artist in data["track"]["album"]["artists"])}
            obj, created = spotify_tracks.objects.update_or_create(
                track_id=data["track"]["id"] if data["track"]["id"] else None,
                defaults=defaults_tracks
            )
            print(obj,created)
            obj.save()

            try:
                defaults = {
                    'timestamp': data["played_at"],
                    'user_id': self.user_id,
                    'playlist_href': data["context"]["href"] if data["context"]["href"] else None,
                    'artist_id': " ".join(artist["id"] for artist in data["track"]["album"]["artists"]),
                    'album_id': data["track"]["album"]["id"] if data["track"]["album"]["id"] else None,
                    'track_id': data["track"]["id"] if data["track"]["id"] else None,
                    'track_name': data["track"]["name"] if data["track"]["name"] else None,
                    'progress_ms': None,
                    'currently_playing_type': None,
                    'is_playing': False,
                }


                obj, created = user_tracks_history.objects.update_or_create(
                    timestamp=data["played_at"],
                    user_id=self.user_id, defaults=defaults
                )
                obj.save()
            except Exception as e:
                print(e)





class SpotifyRefreshUsers():
    def __init__(self):
        self.users = User.objects.all()
        self.refresh_token_url = "https://accounts.spotify.com/api/token"

        self.headers = {'Content-Type': "application/x-www-form-urlencoded",
                        'Authorization': "Basic YTlhODIwM2U2OTdhNDE0MTgyNTNkOTgyMGE4OWYwY2U6MzcxYjM5NTg3ZWJjNDg1NWIzNGE1ZjM2YzdlMjJlZDY=", }


    def refresh_token(self):
        '''
        TO BE CLEANED
        :return:
        '''
        for user in self.users:
            user = User.objects.get(username=user)
            try:
                self.payload = "grant_type=refresh_token&refresh_token="
                self.querystring = {"grant_type": "refresh_token",
                                    "refresh_token": ""}
                social = user.social_auth.get(provider='spotify')
                refresh_token = social.extra_data['refresh_token']
                print(social.extra_data['refresh_token'],social)
                self.querystring["refresh_token"]= refresh_token
                self.payload = self.payload + refresh_token
                response = requests.request("POST", self.refresh_token_url, data=self.payload, headers=self.headers, params=self.querystring)
                data = response.json()
                print(refresh_token)
                print(data,user)
                social.extra_data['access_token'] = data['access_token']
                social.save()
            except Exception as e:
                print(str(e))




