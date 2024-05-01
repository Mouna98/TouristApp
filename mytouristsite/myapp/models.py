from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Visit(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    duration = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Domanda(models.Model):
    testo = models.CharField(max_length=255)
    risposta = models.BooleanField()
    descrizione = models.TextField()

    def __str__(self):
        return self.testo
