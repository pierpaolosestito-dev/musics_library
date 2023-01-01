from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets, generics

from musics.models import CD
from musics.permissions import IsPublisherOrReadOnly
from musics.serializers import CDSerializer, RegistrationSerializer


class CDViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPublisherOrReadOnly | permissions.IsAdminUser]
    queryset = CD.objects.all()
    serializer_class = CDSerializer


# CDByArtist,CDByPublishedBy,CDByName
class CDByArtist(generics.ListAPIView):
    permission_classes = [IsPublisherOrReadOnly | permissions.IsAdminUser]
    model = CD
    serializer_class = CDSerializer

    def get_queryset(self):
        artist = self.request.query_params.get('artist')
        cd_by_artist = CD.objects.filter(artist__icontains=artist)
        return cd_by_artist


class CDByName(generics.ListAPIView):
    permission_classes = [IsPublisherOrReadOnly | permissions.IsAdminUser]
    model = CD
    serializer_class = CDSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        cd_by_name = CD.objects.filter(name__icontains=name)
        return cd_by_name


class CDByPublishedBy(generics.ListAPIView):
    permission_classes = [IsPublisherOrReadOnly | permissions.IsAdminUser]
    model = CD
    serializer_class = CDSerializer

    def get_queryset(self):
        published_by_search = self.request.query_params.get('publishedby')
        published_by_users = User.objects.filter(username__icontains=published_by_search)
        cd_by_published = []
        for u in published_by_users:
            cd_by_published += CD.objects.filter(published_by=u.id)
        return cd_by_published


class RegistrationView(RegisterView):
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        pass
