from django.db import models
from kursy.models import Pytanie

# Create your models here.

class StatystykiPytania(models.Model):
    #class Status(models.TextChoices):
    pytanie = models.OneToOneField(Pytanie,on_delete=models.CASCADE)
    ilosc_odpowiedzi = models.PositiveIntegerField(default=0)
    poprawne_odpowiedzi = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Statystyka Pytania"
        verbose_name_plural = "Statystyki pytania"

    def __str__(self):
        return f"Statystyki dla pytania {self.pytanie}"    