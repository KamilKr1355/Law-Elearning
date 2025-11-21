from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from kursy.models import Artykul, Pytanie, Kurs

# Create your models here.

class ZapisArtykulu(models.Model):
    artykul = models.ForeignKey(Artykul, on_delete=models.CASCADE) 
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    data_zapisu = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ZapisArtykulu"          
        verbose_name_plural = "ZapisyArtykulu" 
        unique_together = ("uzytkownik", "artykul") 
        ordering = ["-data_zapisu"]

    def __str__(self):
        return f"{self.uzytkownik.username} zapisał {self.artykul}"
    
class Notatka(models.Model):
    uzytkownik = models.ForeignKey(User,on_delete=models.CASCADE)
    artykul = models.ForeignKey(Artykul, on_delete=models.CASCADE)
    tresc = models.TextField()
    data_zapisu = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notatka"          
        verbose_name_plural = "Notatki" 
        ordering = ["-data_zapisu"]

    def __str__(self):
        return f"Notatka {self.uzytkownik.username}"

class Komentarz(models.Model):
    uzytkownik = models.ForeignKey(User,on_delete=models.CASCADE)
    artykul = models.ForeignKey(Artykul, on_delete=models.CASCADE)
    tresc = models.TextField()
    data_zapisu = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Komentarz"          
        verbose_name_plural = "Komentarze" 
        ordering = ["-data_zapisu"]

    def __str__(self):
        return f"Komentarz {self.uzytkownik.username}"

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
    
class ProgressPytan(models.Model):
    class Status(models.TextChoices):
        NIEWYSWIETLONE = "NW", "Nie wyswietlone"
        WYSWIETLONE = "W", "Wyswietlone"
        ODP_POPR = "OP", "Poprawna odpowiedz"
        ODP_ZLA = "OZ", "Niepoprawna odpowiedz"
    
    uzytkownik = models.ForeignKey(User,on_delete=models.CASCADE)
    pytanie = models.ForeignKey(Pytanie,on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices = Status,
        default = Status.NIEWYSWIETLONE
    )

    data_aktualizacji = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Postęp pytania"
        verbose_name_plural = "Postępy pytań"
        unique_together = ("uzytkownik", "pytanie")
        ordering = ["-data_aktualizacji"]

    def __str__(self):
        return f"{self.uzytkownik.username} - {self.pytanie} : {self.status}"


class WynikiEgzaminu(models.Model):
    uzytkownik = models.ForeignKey(User,on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    data_zapisu = models.DateTimeField(auto_now_add=True)
    wynik = models.FloatField()

    class Meta:
        verbose_name = "Wynik egzaminu"
        verbose_name_plural = "Wyniki egzaminów"
        ordering = ["-data_zapisu"]

    def __str__(self):
        return f"{self.uzytkownik.username} - {self.wynik}"
    
class OcenaArtykulu(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    artykul = models.ForeignKey(Artykul, on_delete=models.CASCADE)
    ocena = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("uzytkownik", "artykul")

    def __str__(self):
        return f"{self.uzytkownik.username} ocenił {self.artykul} na {self.ocena}"