from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens  import RefreshToken
from django.contrib.auth.models import User
from kursy.models import Kurs
from kursy.api.serializers import OdpowiedzSerializer

class QuizSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tresc = serializers.CharField()
    odpowiedzi = OdpowiedzSerializer(many=True)

    def validate_odpowiedzi(self,value):
        if not any(o['correct'] for o in value):
            raise serializers.ValidationError("Musi byc przynajmniej 1 poprawna odpowiedz")
        return value
    
class SprawdzOdpowiedzSerializer(serializers.Serializer):
    pytanie_id = serializers.IntegerField()
    wybrana_opcja = serializers.IntegerField()

class ZapisArtykuluSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    data_zapisu = serializers.DateTimeField(read_only=True)
    tresc = serializers.CharField(read_only=True)
    tytul = serializers.CharField(read_only=True)


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