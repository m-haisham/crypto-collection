from django.db import models


class HammingSequence(models.Model):
    is_even = models.BooleanField()
    sequence = models.CharField(max_length=124)