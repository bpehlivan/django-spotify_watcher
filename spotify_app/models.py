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
    album_id = models.ForeignKey(spotify_albums, on_delete=models.CASCADE , related_name='album_id_pk')
    artist_id = models.ForeignKey(spotify_tracks, on_delete=models.CASCADE, related_name='artist_id_pk')
    track_name = models.ForeignKey(spotify_tracks, on_delete=models.CASCADE, related_name='track_name_pk')
    track_id = models.ForeignKey(spotify_tracks, on_delete=models.CASCADE, related_name='track_id_pk')
    progress_ms = models.IntegerField()
    currently_playing_type = models.CharField(max_length=255)
    is_playing = models.BooleanField()



class spotify_playlists(models.Model):
    pass

