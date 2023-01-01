from datetime import datetime

from valid8 import ValidationError

from musics_library.domain import ID, Password, Name, Artist, RecordCompany, Genre, Username, EANCode, Price, CD
import pytest


# ID
def test_parse_id_return_correct_id():
    assert ID.parse("10")

def test_negative_id_raises_exception():
    with pytest.raises(ValidationError):
        ID(-1)


def test_positive_id_is_correct():
    correct_values = [1, 2, 3, 4, 5]
    for correct in correct_values:
        assert ID(correct)


def test_str_id():
    assert str(ID(1)) == "1"


# NAME
def test_empty_name_raises_exception():
    with pytest.raises(ValidationError):
        Name("")


def test_name_length_of_51_raises_exception():
    with pytest.raises(ValidationError):
        Name("A" * 51)


def test_name_accepts_some_symbols_like_space_minus_and_comma():
    name_with_symbols = ['Blink!', 'AC-DC', 'Jelly, The Fish!', "@AM"]
    for name in name_with_symbols:
        assert Name(name)


def test_name_str():
    assert str(Name("SSDSBM")) == "SSDSBM"


# ARTIST
def test_empty_artist_name_raises_exception():
    with pytest.raises(ValidationError):
        Artist("")


def test_artist_name_of_length_51_raises_exception():
    with pytest.raises(ValidationError):
        Artist("A" * 51)


def test_artist_name_accepts_some_symbols_like_space_minus_and_comma():
    name_with_symbols = ['Blink!', 'AC-DC', 'Jelly, The Fish!', "@AM"]
    for name in name_with_symbols:
        assert Artist(name)


def test_artist_name_str():
    assert str(Artist("SSDSBM")) == "SSDSBM"


# RECORDCOMPANY
def test_empty_record_company_raises_exception():
    with pytest.raises(ValidationError):
        RecordCompany("")


def test_record_company_of_length_51_raises_exception():
    with pytest.raises(ValidationError):
        RecordCompany("A" * 51)


def test_record_company_accepts_some_symbols_like_space_minus_and_comma():
    name_with_symbols = ['Blink!', 'AC-DC', 'Jelly, The Fish!', "@AM", "#MusiCEnTerTainMEnt"]
    for name in name_with_symbols:
        assert RecordCompany(name)


def test_record_company_str():
    assert str(RecordCompany("SSDSBM - Music Entertainment")) == "SSDSBM - Music Entertainment"


# GENRE
def test_empty_genre_raises_exception():
    with pytest.raises(ValidationError):
        Genre("")


def test_genre_of_length_26_raises_exception():
    with pytest.raises(ValidationError):
        Genre("A" * 26)


def test_genre_accepts_only_whitespaces():
    wrong_values = ["Rock!", "Rock-n-Roll", "Jazz!@", "Blues1"]
    for wrong in wrong_values:
        with pytest.raises(ValidationError):
            Genre(wrong)

    correct_values = ["Rock", "Rock n Roll", "Folk", "Jazz", "Blues", "Heavy Metal"]
    for correct in correct_values:
        assert Genre(correct)


def test_genre_first_letter_is_upper():
    with pytest.raises(ValidationError):
        Genre("rock")
    assert Genre("Rock")


# EAN_CODE
@pytest.mark.parametrize("ean_code", [("978020137962"), ("1845678901001")])
def test_correct_ean_code(ean_code):
    assert EANCode(ean_code)


@pytest.mark.parametrize("wrong_ean_code", [("124214"), ("1234567"), ("1234567810")])
def test_wrong_ean_code_raises_exception(wrong_ean_code):
    with pytest.raises(Exception):
        EANCode(wrong_ean_code)


def test_str_ean_code():
    assert str("978020137962") == "978020137962"


def test_genre_str():
    assert str(Genre("Rock")) == "Rock"


# PRICE
def test_price_no_init():
    with pytest.raises(ValidationError):
        Price(1)


def test_price_cannot_be_negative():
    with pytest.raises(ValidationError):
        Price.create(-1, 0)


def test_price_no_cents():
    assert Price.create(1, 0) == Price.create(1)


def test_price_parse():
    assert Price.parse('10.20') == Price.create(10, 20)


def test_price_str():
    assert str(Price.create(9, 99)) == '9.99'


def test_price_euro():
    assert Price.create(11, 22).euro == 11


def test_price_cents():
    assert Price.create(11, 22).cents == 22


def test_price_add():
    assert Price.create(9, 99).add(Price.create(0, 1)) == Price.create(10)


def test_price_omitted_cents():
    assert Price.create(11)


# USERNAME
def test_empty_username_raises_exception():
    with pytest.raises(ValidationError):
        Username("")


def test_username_of_length_151_raises_exception():
    with pytest.raises(ValidationError):
        Username("A" * 151)


def test_str_username():
    assert str(Username("ssdsbm")) == "ssdsbm"


def test_username_only_accepts_characters_and_numbers():
    wrong_values = ["u'@-sername", "u\sername123", "u!ser"]
    for wrong in wrong_values:
        with pytest.raises(ValidationError):
            Username(wrong)
    correct_values = ['username123', 'Ricky1', "ssdsbm14"]
    for correct in correct_values:
        assert Username(correct)


# PASSWORD
@pytest.mark.parametrize("wrong_passwords", [("A"), ("aa@"), ("Aa "), ("A-!@"), ("Aaaaa"), ("Aaa aa"), ("Aaaaaaa")])
def test_password_has_min_length_of_8(wrong_passwords):
    with pytest.raises(ValueError):
        Password(wrong_passwords)
    assert Password("Abcd!-@.")


def test_password_length_of_129_raises_exception():
    with pytest.raises(ValueError):
        Password("A" * 128 + "a")


def test_password_with_spaces_raises_exception():
    with pytest.raises(ValueError):
        Password("A" * 6 + " " + "a")


def test_cd_with_id_and_created_at_and_updated_at_setted_with_default_values():
    cd = CD(Name("Ciao"), Artist("Bino"), RecordCompany("BinoRecord"), Genre("Rock"), EANCode("978020137962"),
               Price.create(10, 20))

    assert cd.music_id == 1898989

    assert cd.publishedby == "music-library"

    assert cd.created_at.day == datetime.now().day
    assert cd.created_at.month == datetime.now().month
    assert cd.created_at.year == datetime.now().year
    assert cd.created_at.time().hour == datetime.now().time().hour
    assert cd.created_at.time().minute == datetime.now().time().minute

    assert cd.updated_at.day == datetime.now().day
    assert cd.updated_at.month == datetime.now().month
    assert cd.updated_at.year == datetime.now().year
    assert cd.updated_at.time().hour == datetime.now().time().hour
    assert cd.updated_at.time().minute == datetime.now().time().minute


def test_cd_with_all_fields():
    assert CD(ID(1), Name("Ciao"), Artist("Bino"), RecordCompany("BinoRecord"), Genre("Rock"),
              EANCode("978020137962"), Username("ssdsbm-test"), Price.create(10, 20), datetime.now(), datetime.now())


def test_str_cd():
    music = CD(Name("Ciao"), Artist("Bino"), RecordCompany("BinoRecord"), Genre("Rock"), EANCode("978020137962"),
               Price.create(10, 20))
    assert str(
        music) == "CD Name: Ciao Artist: Bino Record Company: BinoRecord Genre: Rock EANCode: 978020137962 Price: 10.20"


def test_cd_created_at():
    assert CD(ID(1), Name("Ciao"), Artist("Bino"), RecordCompany("BinoRecord"), Genre("Rock"),
              EANCode("978020137962"), Username("ssdsbm-test"), Price.create(10, 20), datetime.now(),
              datetime.now()).createdat == datetime.now().strftime('%d-%m-%Y %H:%M')


def test_cd_updated_at():
    assert CD(ID(1), Name("Ciao"), Artist("Bino"), RecordCompany("BinoRecord"), Genre("Rock"),
              EANCode("978020137962"), Username("ssdsbm-test"), Price.create(10, 20), datetime.now(),
              datetime.now()).updatedat == datetime.now().strftime('%d-%m-%Y %H:%M')
