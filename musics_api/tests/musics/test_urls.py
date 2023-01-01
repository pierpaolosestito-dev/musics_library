import json
from urllib.parse import urlencode

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient


@pytest.fixture()
def musics(db):
    user_one = mixer.blend(get_user_model())
    group = mixer.blend(Group, name="publishers")
    user_one.groups.add(group)

    return [
        mixer.blend('musics.CD'),
        mixer.blend('musics.CD'),
        mixer.blend('musics.CD'),
        mixer.blend('musics.CD',artist="PinkFloyd"),
        mixer.blend('musics.CD',artist="PinkFloyd",name="A",published_by=user_one)
    ]

@pytest.fixture()
def users(db):
    user_one = mixer.blend(get_user_model())
    group = mixer.blend(Group, name="publishers")
    user_one.groups.add(group)
    return user_one

@pytest.fixture()
def musics_with_published_by(db):
    user_one = mixer.blend(get_user_model())
    user_two = mixer.blend(get_user_model())
    group = mixer.blend(Group, name="publishers")
    user_one.groups.add(group)
    user_two.groups.add(group)

    return [
        mixer.blend('musics.CD', published_by=user_one),
        mixer.blend('musics.CD', published_by=user_two)
    ]


def get_client(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


def test_musics_anon_user_get_403_with_POST():
    path = reverse('musics-list')
    client = get_client()
    response = client.post(path)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_musics_anon_user_get_403_with_DELETE(musics):
    path = reverse('musics-detail', kwargs={'pk': musics[0].pk})
    client = get_client()
    response = client.delete(path)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_musics_anon_user_get_403_with_PUT(musics):
    path = reverse('musics-detail', kwargs={'pk': musics[0].pk})
    client = get_client()
    response = client.put(path)
    assert response.status_code == HTTP_403_FORBIDDEN

def test_musics_anon_user_get_200_with_GET(musics):
    path = reverse('musics-list') #/musics/byartist?artist=
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(musics)
def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


def test_musics_anon_user_get_200_with_GET_by_artist(musics):
    path = reverse_querystring('byartist',query_kwargs={'artist':musics[4].artist})
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == 2

def test_musics_anon_user_get_200_with_GET_by_name(musics):
    path = reverse_querystring('byname',query_kwargs={'name':musics[4].name})
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_200_OK

def test_musics_anon_user_get_200_with_GET_by_published_by(musics):
    path = reverse_querystring('bypublishedby',query_kwargs={'publishedby':musics[4].published_by})
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_200_OK

def test_musics_anon_user_get_200_with_GET_a_single_post(musics):
    path = reverse('musics-detail', kwargs={'pk': musics[0].pk})
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert obj['artist'] == musics[0].artist


def test_musics_auth_user_get_403_on_other_published_musics_with_PUT(musics_with_published_by):
    path = reverse('musics-detail', kwargs={'pk': musics_with_published_by[1].pk})
    client = get_client(musics_with_published_by[0].published_by)
    response = client.put(path)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_musics_auth_user_get_403_on_other_published_musics_with_DELETE(musics_with_published_by):
    path = reverse('musics-detail', kwargs={'pk': musics_with_published_by[1].pk})
    client = get_client(musics_with_published_by[0].published_by)
    response = client.delete(path)
    assert response.status_code == HTTP_403_FORBIDDEN


# def tests_musics_auth_user_get_200_on_own_published_musics_with_PUT(musics_with_published_by):
#      path = reverse('musics-detail', kwargs={'pk': musics_with_published_by[0].pk})
#      client = get_client(musics_with_published_by[0].published_by)
#      #print(json.dumps(mixer.blend('musics.CD',artist="Pink Floyd")))
#      datas = serializers.serialize('json', mixer.blend('musics.CD',artist='Pink Floyd',))
#      response = client.put(path,data=datas)
#      assert response.status_code == HTTP_200_OK

def tests_musics_auth_user_get_200_on_own_published_musics_with_DELETE(musics_with_published_by):  # da sistemare
    path = reverse('musics-detail', kwargs={'pk': musics_with_published_by[0].pk})
    client = get_client(musics_with_published_by[0].published_by)
    response = client.delete(path)
    assert response.status_code == HTTP_204_NO_CONTENT


def tests_music_anon_user_get_403_on_POST():
    path = reverse('musics-list')
    client = get_client()
    response = client.post(path)
    assert response.status_code == HTTP_403_FORBIDDEN

