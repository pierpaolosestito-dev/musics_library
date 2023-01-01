from musics_library.mappers import CDMapper
from musics_library.domain import *
import pytest


def test_music_mapper_from_fake_json():
    c = CDMapper()
    c.map_cd({
        "id": 39,
        "name": "Ciao",
        "artist": "Ciao2",
        "record_company": "Ciao",
        "genre": "CIao",
        "ean_code": "978020137962",
        "price": "10.00",
        "price_currency": "EUR",
        "published_by": 3,
        "user": "ssdsbm2",
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now())
    }) == CD(id=ID(39), name=Name("Ciao"), artist=Artist("Ciao"), record_company=RecordCompany("Ciao"), genre=Genre("Ciao"), ean_code=EANCode("978020137962"), price=Price.parse("10.00"), published_by=Username("ssdsbm2"), created_at=datetime.now(), updated_at=datetime.now())