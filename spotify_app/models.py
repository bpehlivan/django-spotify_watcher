from django.db import models


class spotify_tracks(models.Model):
    track_id = models.CharField(max_length=255, primary_key=True)
    track_name = models.CharField(max_length=255)
    track_popularity = models.CharField(max_length=255)
    track_duration = models.CharField(max_length=255)
    track_uri = models.CharField(max_length=255)
    track_href = models.CharField(max_length=255)
    track_artist_id = models.CharField(max_length=255)
    track_artist_name = models.CharField(max_length=255)

class spotify_albums(models.Model):
    album_id = models.CharField(max_length=255, primary_key=True)
    album_name = models.CharField(max_length=255)
    album_uri = models.CharField(max_length=255)
    album_artists_ids = models.CharField(max_length=255)
    album_href = models.CharField(max_length=255)

class user_tracks_history(models.Model):
    timestamp = models.DateTimeField()
    user_id = models.IntegerField()
    playlist_href = models.CharField(max_length=255)
    album_id = models.CharField(max_length=255)
    artist_id = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    track_id = models.CharField(max_length=255)
    progress_ms = models.IntegerField(blank=True, null=True)
    currently_playing_type = models.CharField(max_length=255,blank=True, null=True)
    is_playing = models.BooleanField(blank=True, null=True)



class spotify_playlists(models.Model):
    pass

