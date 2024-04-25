from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Visit(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    duration = models.IntegerField(default=1, validators=[MinValueValidator(1)])  # assuming duration is in days

    def __str__(self):
        return self.name
