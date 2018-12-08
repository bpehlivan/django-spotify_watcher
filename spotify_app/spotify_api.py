import json
import logging
import requests
from datetime import datetime
from django.contrib.auth.models import User

from .models import user_tracks_history
from spotify_app.api_spotify_wrapper import Spotify
# ts = int("1284101485")
# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

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
        self.user_id = user_object.id

    def get_currently_playing(self):

        print(self.auth_token)
        print(self.user_id)
        url = "https://api.spotify.com/v1/me/player/currently-playing"
        payload = ""
        headers = {'Authorization': "Bearer " + "BQBMsvit6meAnrZykmbBcw1sdSwLDXUXMZcZhiGAfxrkWSNd2Ah3J5KJ7g8aLj8xGJD6f5B491dMeR80NZtCjcc0Hlg8K2SdrxHj2ie0VzBl1evWbubd9VybOxWOSpHIxkJx5UPVbsuvc6UsDkEv9tJh3GLD0f-5Snk6dd8qiPRS40KvLqTvQ9u4nC8Rbwf9Z2rCeMx8JcEmOmVm650bS7WGwUV6WaBqdumlkg7lUHr8pGHeeom5",
                   'cache-control': "no-cache"}

        response = requests.request("GET", url, data=payload, headers=headers)

        data = response.text
        #logger.info(data)
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
            logger.info("DATA " +  data["item"]["name"] + ' ' + self.user_id)
        except Exception as e:
            print(str(e))
            logger.warning('NO DATA' + self.user_id)


    def test_api(self):
        x=Spotify(auth="BQBMsvit6meAnrZykmbBcw1sdSwLDXUXMZcZhiGAfxrkWSNd2Ah3J5KJ7g8aLj8xGJD6f5B491dMeR80NZtCjcc0Hlg8K2SdrxHj2ie0VzBl1evWbubd9VybOxWOSpHIxkJx5UPVbsuvc6UsDkEv9tJh3GLD0f-5Snk6dd8qiPRS40KvLqTvQ9u4nC8Rbwf9Z2rCeMx8JcEmOmVm650bS7WGwUV6WaBqdumlkg7lUHr8pGHeeom5").current_user_recently_played()
        print(type(x))
        logger.info(json.dumps(x))


class SpotifyRefreshUsers():
    def __init__(self):
        self.users = User.objects.all()
        self.refresh_token_url = "https://accounts.spotify.com/api/token"
        self.headers = {'Content-Type': "application/x-www-form-urlencoded",
                        'Authorization': "Basic YTlhODIwM2U2OTdhNDE0MTgyNTNkOTgyMGE4OWYwY2U6MzcxYjM5NTg3ZWJjNDg1NWIzNGE1ZjM2YzdlMjJlZDY=", }
        self.payload = "grant_type=refresh_token&refresh_token="

    def refresh_token(self):
        print(self.users)
        for user in self.users:
            user = User.objects.get(username=user)
            try:
                social = user.social_auth.get(provider='spotify')
                refresh_token = social.extra_data['refresh_token']
                self.payload = self.payload + refresh_token
                response = requests.request("POST", self.refresh_token_url, data=self.payload, headers=self.headers)
                data = response.json()
                social.extra_data['access_token'] = data['access_token']
                social.save()
            except Exception as e:
                print(str(e))




