from django.db import models

# Create your models here.
class user_tracks(models.Model):
    pass

class user_tracks_history(models.Model):
    timestamp = models.DateTimeField()
    user_id = models.IntegerField()
    playlist_href = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=255)
    album_id = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    track_id = models.CharField(max_length=255)
    progress_ms = models.IntegerField()
    currently_playing_type = models.CharField(max_length=255)
    is_playing = models.BooleanField()

class spotify_tracks(models.Model):
    pass


class spotify_playlists(models.Model):
    pass

