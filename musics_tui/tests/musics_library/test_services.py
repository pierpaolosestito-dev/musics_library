import os

import dotenv
import pytest

from musics_library.domain import Username, ID, Price, EANCode, Genre, RecordCompany, Artist, Name, CD, Password
from musics_library.services import AuthenticatedUser, CDService, CDByPublishedByService, CDByArtistService, \
    ApiException, CDByNameService, AuthenticationService


@pytest.fixture
def load_dotenv():
    yield dotenv.load_dotenv()


def test_dotenv(load_dotenv):
    assert os.getenv('ROOT_ENDPOINT') == "http://localhost:8000"
    assert os.getenv('MUSIC_ENDPOINT') == "http://localhost:8000/api/v1/musics/"
    assert os.getenv('AUTH_ENDPOINT') == "http://localhost:8000/api/v1/auth/"


def test_str_authenticated_user():
    assert str(
        AuthenticatedUser('eyJhbGciOiJIUzI1NiIsInR5c', ID(1), Username("ssdsbm28"),True,True)) == "eyJhbGciOiJIUzI1NiIsInR5c 1 True"


def test_musics_service_fetch_musics_detail_wrong_url_raises_exception(requests_mock):
    with pytest.raises(ApiException):
        id = ID(49)
        requests_mock.get("http://localhost:8000/api/v1/musics/" + str(id.value) + "/a", json="")
        ms = CDService()
        resp = ms.fetch_cd_detail(id)


def test_musics_service_fetch_musics_list(requests_mock):
    requests_mock.get("http://localhost:8000/api/v1/musics/", json="")
    ms = CDService()
    resp = ms.fetch_cd_list()
    assert resp != None


def test_musics_service_by_publisher_fetch_musics_list(requests_mock):
    published_by = Username("ssdsbm")
    requests_mock.get("http://localhost:8000/api/v1/musics/by_published_by?publishedby=" + published_by.value, json="")
    ms = CDByPublishedByService()
    resp = ms.fetch_cd_by_published_by_list(published_by)
    assert resp != None


def test_musics_service_by_artist_fetch_musics_list(requests_mock):
    artist = Artist("ssdsbm")
    requests_mock.get("http://localhost:8000/api/v1/musics/byartist?artist=" + artist.value, json="")
    ms = CDByArtistService()
    resp = ms.fetch_cd_by_artist_list(artist)
    assert resp != None


def test_musics_service_by_cd_name_fetch_musics_list(requests_mock):
    cd_name = Name("ssdsbm")
    requests_mock.get("http://localhost:8000/api/v1/musics/byname?name=" + cd_name.value,
                      json="")
    ms = CDByNameService()
    resp = ms.fetch_cds_by_name_list(cd_name)
    assert resp != None


def test_musics_services_wrong_url_raises_api_exception(requests_mock):
    with pytest.raises(ApiException):
        requests_mock.get("http://localhost:8000/api/v1/musics/wrong_path", json="")
        ms = CDService()
        resp = ms.fetch_cd_list()


def test_musics_services_by_artist_wrong_url_raises_api_exception(requests_mock):
    with pytest.raises(ApiException):
        artist = Artist("ssdsbm")
        requests_mock.get("http://localhost:8000/api/v1/musics/byarattist?artist=" + artist.value, json="")
        ms = CDByArtistService()
        resp = ms.fetch_cd_by_artist_list(artist)


def test_musics_services_by_published_by_wrong_url_raises_api_exception(requests_mock):
    with pytest.raises(ApiException):
        published_by = Username("ssdsbm")
        requests_mock.get("http://localhost:8000/api/v1/musics/by_published_byyyy?published_by=" + published_by.value,
                          json="")
        ms = CDByPublishedByService()
        resp = ms.fetch_cd_by_published_by_list(published_by)


def test_musics_services_by_cd_name_wrong_url_raises_api_exception(requests_mock):
    with pytest.raises(ApiException):
        cd_name = Name("ssdsbm")
        requests_mock.get("http://localhost:8000/api/v1/musics/bynamee?published_by=" + cd_name.value,
                          json="")
        ms = CDByNameService()
        resp = ms.fetch_cds_by_name_list(cd_name)


def test_authentication_service_correct_login(requests_mock):
    requests_mock.post(url="http://localhost:8000/api/v1/auth/login/",
                       json={"key": "abCde", "user": {"id": 1, "username": "ssdsbm","is_superuser":True,"groups":[{"name":"publishers"}]}})
    auth_service = AuthenticationService()
    resp = auth_service.login(Username("sssbm"), Password("ssdsbm1234"))
    assert resp != None


def test_authentication_service_correct_logout(requests_mock):
    requests_mock.post(url="http://localhost:8000/api/v1/auth/logout/",
                       json="Logout successfull")
    auth_service = AuthenticationService()
    resp = auth_service.logout(AuthenticatedUser("abCd", ID(1), Username("ssdsbm"),True,True))
    assert resp != None


def test_authentication_service_wrong_login_raises_exception(requests_mock):
    requests_mock.post(url="http://localhost:8000/api/v1/auth/login/",
                       json={}, status_code=400)
    with pytest.raises(ApiException):
        auth_service = AuthenticationService()
        resp = auth_service.login(Username("sssbm"), Password("ssdsbm1234"))


def test_authentication_service_wrong_logout_raises_exception(requests_mock):
    requests_mock.post(url="http://localhost:8000/api/v1/auth/logout/",
                       json={}, status_code=400)
    with pytest.raises(ApiException):
        auth_service = AuthenticationService()
        resp = auth_service.logout(AuthenticatedUser("abCd", ID(1), Username("ssdsbm"),True,True))


def test_musics_service_add_music_raises_exception(requests_mock):
    with pytest.raises(ApiException):
        requests_mock.post(url="http://localhost:8000/api/v1/musics/",
                           json={
                               "id": 41,
                               "name": "Mod",
                               "artist": "Ciao",
                               "record_company": "Ciao",
                               "genre": "Rock",
                               "ean_code": "978020137962",
                               "price": "15.00",
                               "price_currency": "EUR",
                               "published_by": 1,
                               "user": "ssdsbm",
                               "created_at": "2022-12-04T17:27:28.325209Z",
                               "updated_at": "2022-12-09T14:13:02.610624Z"
                           }, )
        ms = CDService()
        resp = ms.add_cd(
            CD(id=ID(1), name=Name("Mod"), artist=Artist("Ciao"), record_company=RecordCompany("Ciao"),
               genre=Genre("Rock"), ean_code=EANCode("978020137962"), price=Price.parse("15.00")),
            auth_user=AuthenticatedUser("kkbb", ID(1), Username("ciao"),True,True))


