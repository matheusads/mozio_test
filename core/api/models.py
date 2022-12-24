import uuid

from django.conf.global_settings import LANGUAGES
from django.contrib.gis.db import models as gis_models
from django.db import models


class Provider(models.Model):
    CURRENCY_CHOICES = (
        ('US Dollars', 'USD'),
        ('Euro', 'EUR'),
        ('Great Britain Pound', 'GBP'),
        ('Brazilian Real', 'BRL'),
    )

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          unique=True,
                          editable=False)
    name = models.CharField("Provider Name", max_length=255)
    email = models.EmailField("Provider Email", unique=True, max_length=255)
    phone_number = models.CharField("Provider Phone Number", max_length=255)
    language = models.CharField("Provider Language",
                                max_length=10,
                                choices=LANGUAGES,
                                default='en')
    currency = models.CharField(
        "Provider Currency",
        default='USD',
        choices=CURRENCY_CHOICES,
        max_length=20)  # one option is use django-money instead

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class ServiceArea(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          unique=True,
                          editable=False)
    provider = models.ForeignKey('Provider',
                                 on_delete=models.CASCADE,
                                 related_name='service_areas')
    name = models.CharField("Name", max_length=100)
    price = models.DecimalField("Price", max_digits=100, decimal_places=2)
    polygon = gis_models.PolygonField("Polygon", geography=True)
