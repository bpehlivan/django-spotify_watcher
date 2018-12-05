from django.contrib.auth.models import User, Group
from spotify_app.models import user_tracks_history
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class user_track_history_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_tracks_history
        fields = ('user_id','timestamp','track_name','album_id')

