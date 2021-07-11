from django.db import models


class CreditCard(models.Model):
    name = models.CharField(max_length=32)
    thumbnail_link = models.CharField(max_length=64)


class CreditCardType:
    amex = 1
    master_card = 2
    visa = 3
    discover = 4
