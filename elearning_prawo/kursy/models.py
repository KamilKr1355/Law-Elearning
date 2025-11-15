from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Kurs(models.Model):
    uzytkownik = models.ManyToManyField(User, through='Uzytkownik_kurs')
    nazwa_kursu = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Kurs"          
        verbose_name_plural = "Kursy"   

    def __str__(self):
        return self.nazwa_kursu
    
class Uzytkownik_kurs(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    data_zapisu = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uzytkownik', 'kurs')
        verbose_name = "Uzytkownik_kurs"          
        verbose_name_plural = "Uzytkownik_kursy"   

class Rozdzial(models.Model):
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    nazwa_rozdzialu = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Rozdzial"          
        verbose_name_plural = "Rozdzialy" 

    def __str__(self):
        return f"{self.kurs.nazwa_kursu} - {self.nazwa_rozdzialu}"

class Artykul(models.Model):
    rozdzial = models.ForeignKey(Rozdzial, on_delete=models.CASCADE)
    tresc = models.TextField()
    tytul = models.TextField()
    nr_artykulu = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Artykul"          
        verbose_name_plural = "Artykuly" 

    def __str__(self):
        return f"{self.nr_artykulu} {self.tytul}"

class Pytanie(models.Model):
    artykul = models.ForeignKey(Artykul, on_delete=models.CASCADE)
    tresc = models.TextField()

    class Meta:
        verbose_name = "Pytanie"          
        verbose_name_plural = "Pytania" 

    def __str__(self):
        return self.tresc

class Odpowiedz(models.Model):
    pytanie = models.ForeignKey(Pytanie,on_delete=models.CASCADE)
    tresc = models.TextField()
    poprawna = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Odpowiedz"          
        verbose_name_plural = "Odpowiedzi" 

    def __str__(self):
        return self.tresc

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