from django.core.exceptions import ValidationError
from stdnum.util import clean, isdigits
import re


def validate_name(value: str) -> None:
    if len(value) == 0:
        raise ValidationError('Name must not be empty')
    if not re.match("[A-Za-z0-9- ,'!@]*$", value):
        raise ValidationError(
            "Name format can contain only letters,numbers and special characters as '-', ',' and whitespaces")

def validate_artist(value: str) -> None:
    if len(value) == 0:
        raise ValidationError('Artist name must not be empty')
    if not re.match('[A-Za-z0-9- ,!@]*$', value):
        raise ValidationError(
            "Artist name format can contain only letters,numbers and special characters as '-', ',' and whitespaces")


def validate_record_company(value: str) -> None:
    if len(value) == 0:
        raise ValidationError('Record company name must not be empty')
    if not re.match('[A-Za-z0-9- ,!@#]*$', value):
        raise ValidationError(
            "Record company name format can contain only letters,numbers and special characters as '-', ',' and whitespaces")


def validate_genre(value: str) -> None:
    if len(value) == 0:
        raise ValidationError('Genre name must not be empty')
    if not value[0].isupper():
        raise ValidationError('Genre must be capitalized')
    if not re.match('[a-zA-Z ]*$', value):
        raise ValidationError("Genre name format can contain only letters and whitespaces")


def ean_calc_check_digit(number: str):
    return str((10 - sum((3, 1)[i % 2] * int(n)
                         for i, n in enumerate(reversed(number)))) % 10)


def validate_ean(number: str):
    if not isdigits(number):
        raise ValidationError("EANCode is structured with numbers.")
    if len(number) not in (14, 13, 12, 8):
        raise ValidationError("EANCode length isn't correct.")
    if ean_calc_check_digit(number[:-1]) != number[-1]:
        raise ValidationError("Checksum fails.")


def ean_is_valid(number: str):
    try:
        validate_ean(number)
        return True
    except ValidationError:
        return False
