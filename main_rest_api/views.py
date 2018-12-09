from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, user_track_history_serializer,online_user_live_listenings_serializer
from spotify_app.models import user_tracks_history
from datetime import timedelta, datetime as dt
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class user_track_history(viewsets.ModelViewSet):

    serializer_class = user_track_history_serializer

    def get_queryset(self):
        """
        Returns the last 30 days user track history for requested user
        Dev notes=Timedelta might be changed from interface or settings.py
        """
        user = self.request.user
        return user_tracks_history.objects.filter(user_id=user.id,
                                                  timestamp__range=(dt.now()-timedelta(days=30), dt.now()))


class admin_user_track_history(viewsets.ModelViewSet):
    #permission_classes = (permissions.IsAdminUser,)
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = user_track_history_serializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return user_tracks_history.objects.filter(user_id= user_id,
                                                  timestamp__range=(dt.now() - timedelta(days=30), dt.now()))

###i added timeslot -3 since dt now gives current timezone
class online_user_live_listenings(viewsets.ModelViewSet):
    #permission_classes = (permissions.IsAdminUser,)
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = online_user_live_listenings_serializer

    def get_queryset(self):
        return user_tracks_history.objects.order_by('user_id', '-timestamp').distinct('user_id').filter(timestamp__gte= (dt.now()-timedelta(hours=3)) - timedelta(seconds=60 * 5))

