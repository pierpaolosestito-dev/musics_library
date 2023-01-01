from django.urls import path
from rest_framework.routers import SimpleRouter

from musics.views import CDViewSet, CDByArtist, CDByName, CDByPublishedBy

router = SimpleRouter()
router.register('', CDViewSet, basename="musics")
urlpatterns = [
    path('byartist', CDByArtist.as_view(),name="byartist"),
    path('byname', CDByName.as_view(),name="byname"),
    path('by_published_by', CDByPublishedBy.as_view(),name="bypublishedby")
]
urlpatterns += router.urls
