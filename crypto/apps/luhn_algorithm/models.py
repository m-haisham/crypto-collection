from django.db import models


class CreditCard(models.Model):
    name = models.CharField(max_length=32)
    thumbnail_link = models.CharField(max_length=64)


class CreditCardIssuer:
    amex = 1
    master_card = 2
    visa = 3
    discover = 4
    electron = 5
    maestro = 6
    dankort = 7
    interpayment = 8
    unionpay = 9
    diners = 10
    jcb = 11
