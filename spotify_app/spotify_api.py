from django.contrib.auth.models import User
import requests


import logging

# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
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
    def __init__(self,auth_token,refresh_token):
        self.auth_token=auth_token
        self.refresh_token=refresh_token

    def get_playlists(self):

        url = "https://api.spotify.com/v1/me/player/currently-playing"

        payload = ""
        headers = {
            'Authorization': "Bearer " + self.auth_token,
                             'cache-control': "no-cache",
        }

        response = requests.request("GET", url, data=payload, headers=headers)

        data = response.text
        logger.info(data)



class SpotifyRefreshUsers():
    def __init__(self):
        self.users=User.objects.all()
        self.refresh_token_url="https://accounts.spotify.com/api/token"
        self.headers={  'Content-Type': "application/x-www-form-urlencoded",
                        'Authorization': "Basic YTlhODIwM2U2OTdhNDE0MTgyNTNkOTgyMGE4OWYwY2U6MzcxYjM5NTg3ZWJjNDg1NWIzNGE1ZjM2YzdlMjJlZDY=",}
        self.payload="grant_type=refresh_token&refresh_token="
    def refresh_token(self):
        print(self.users)
        for user in self.users:
            user = User.objects.get(username=user)
            try:
                social = user.social_auth.get(provider='spotify')
                refresh_token = social.extra_data['refresh_token']
                self.payload = self.payload  + refresh_token
                response = requests.request("POST", self.refresh_token_url, data=self.payload, headers=self.headers)
                data=response.json()
                social.extra_data['access_token']=data['access_token']
                social.save()
            except Exception as e:
                print(str(e))


