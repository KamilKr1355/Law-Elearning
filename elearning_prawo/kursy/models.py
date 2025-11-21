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

