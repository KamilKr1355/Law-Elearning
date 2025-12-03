from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens  import RefreshToken
from django.contrib.auth.models import User
from kursy.models import Kurs
from kursy.api.serializers import QuizOdpowiedzSerializer

class QuizSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tresc = serializers.CharField()
    odpowiedzi = QuizOdpowiedzSerializer(many=True)

    """    def validate_odpowiedzi(self,value):
        if not any(o['correct'] for o in value):
            raise serializers.ValidationError("Musi byc przynajmniej 1 poprawna odpowiedz")
        return value
    """

    
class SprawdzOdpowiedzSerializer(serializers.Serializer):
    pytanie_id = serializers.IntegerField()
    wybrana_opcja = serializers.IntegerField()

class ZapisArtykuluSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    data_zapisu = serializers.DateTimeField(read_only=True)
    tresc = serializers.CharField(read_only=True)
    tytul = serializers.CharField(read_only=True)
    artykul_id = serializers.IntegerField()


class ZapisArtykuluPostSerializer(serializers.Serializer):
    artykul_id = serializers.IntegerField()

class NotatkaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tresc = serializers.CharField()
    uzytkownik_id = serializers.IntegerField(read_only=True)
    artykul_id = serializers.IntegerField()
    data_zapisu = serializers.DateTimeField(read_only=True)

class NotatkaPostSerializer(serializers.Serializer):
    tresc = serializers.CharField()
    artykul_id = serializers.IntegerField()

class NotatkaPutSerializer(serializers.Serializer):
    tresc = serializers.CharField()

class KomentarzSerializer(serializers.Serializer):
     id = serializers.IntegerField(read_only=True)
     tresc = serializers.CharField()
     uzytkownik_id = serializers.IntegerField(read_only=True)
     artykul_id = serializers.IntegerField(read_only=True)
     data_zapisu = serializers.DateTimeField(read_only=True)
     username = serializers.CharField(read_only=True)  

class WynikiEgzaminuSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    data_zapisu = serializers.DateTimeField(read_only=True)
    wynik = serializers.FloatField()
    kurs_id = serializers.IntegerField()
    uzytkownik_id = serializers.IntegerField(read_only=True)


class AverageUzytkownikKursSerializer(serializers.Serializer):
    srednia = serializers.FloatField()
    kurs_id = serializers.IntegerField()
    uzytkownik_id = serializers.IntegerField()
    username = serializers.CharField()


class AverageKursSerializer(serializers.Serializer):
    srednia_wynik = serializers.FloatField()
    kurs_id = serializers.IntegerField()

class OcenaArtykuluSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ocena = serializers.IntegerField(min_value=1, max_value=5)
    data_zapisu = serializers.DateTimeField(read_only=True) 
    artykul_id = serializers.IntegerField(read_only=True)
    uzytkownik_id = serializers.IntegerField(read_only=True)

class OcenaArtykuluInputSerializer(serializers.Serializer):
    ocena = serializers.IntegerField(min_value=1, max_value=5)

class OcenaArtykuluCombinedSerializer(serializers.Serializer):
    artykul_id = serializers.IntegerField(read_only=True)
    srednia_ocena = serializers.FloatField(read_only=True) 
    moja_ocena = OcenaArtykuluSerializer(allow_null=True) 

class ProgressPytanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    pytanie_id = serializers.IntegerField()
    status = serializers.CharField(max_length=2) 
    data_aktualizacji = serializers.DateTimeField(read_only=True)

class ProgressKursSummarySerializer(serializers.Serializer):
    total_questions = serializers.IntegerField()
    completed_count = serializers.IntegerField()
    progress_percentage = serializers.FloatField(read_only=True) 

class PytanieTrybNaukiSerializer(serializers.Serializer):
    pytanie_id = serializers.IntegerField()
    tresc = serializers.CharField()
    status_uzytkownika = serializers.CharField(max_length=2) 