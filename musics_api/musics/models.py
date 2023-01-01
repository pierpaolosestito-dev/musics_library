from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator

from musics.validators import validate_name, validate_artist, validate_record_company, validate_genre, \
    validate_ean


# CD:#
# - Nome ->
# - Band/Artista
# - Casa discografica
# - Categoria
# - Codice(UPC/EAN)
# - Prezzo
# - Pubblicato_da
class CD(models.Model):
    name = models.CharField(max_length=50, validators=[validate_name])
    artist = models.CharField(max_length=50, validators=[validate_artist])
    record_company = models.CharField(max_length=50, validators=[validate_record_company])
    genre = models.CharField(max_length=25, validators=[validate_genre])
    ean_code = models.CharField(max_length=13, validators=[validate_ean])
    published_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    price = MoneyField(default=1, default_currency='EUR', max_digits=8, decimal_places=2, validators=[
        MinMoneyValidator(1),
        MaxMoneyValidator(10000),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist + " " + self.name
