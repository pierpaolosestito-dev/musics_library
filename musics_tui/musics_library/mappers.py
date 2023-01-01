from musics_library.domain import CD, ID, Name, Artist, RecordCompany, Genre, EANCode, Username, Price
from dateutil import parser
import musics_library.services as services


class CDMapper:
    @staticmethod
    def map_cd(res):
        created_at = parser.parse(res['created_at'])
        updated_at = parser.parse(res['updated_at'])
        cd = CD(
            id=ID(res['id']),
            name=Name(res['name']),
            artist=Artist(res['artist']),
            record_company=RecordCompany(res['record_company']),
            genre=Genre(res['genre']),
            ean_code=EANCode(res['ean_code']),
            published_by=Username(res['user']),
            price=Price.parse(res['price']),
            created_at=created_at,
            updated_at=updated_at
        )
        return cd


class AuthenticatedUserMapper:
    @staticmethod
    def map_auth_user(res):
        is_publisher = False
        if {'name':'publishers'} in res.json()['user']['groups']:
            is_publisher = True
        return services.AuthenticatedUser(res.json()["key"], ID(res.json()['user']['id']),
                                          Username(res.json()['user']['username']),res.json()['user']['is_superuser'],is_publisher)
