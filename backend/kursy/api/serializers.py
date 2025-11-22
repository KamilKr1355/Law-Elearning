from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens  import RefreshToken
from django.contrib.auth.models import User
from kursy.models import Kurs

    
class KursSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nazwa_kursu = serializers.CharField(max_length=50,required=True)

    def validate_nazwa_kursu(self, value):
        if value is None or value.strip() == "":
            raise serializers.ValidationError("Nazwa kursu nie może być pusta!")
        return value
    
class ArtykulSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tresc = serializers.CharField(required=True,allow_blank=False)
    tytul = serializers.CharField(max_length=50,required=True)
    nr_artykulu = serializers.CharField(max_length=10)
    rozdzial_id = serializers.IntegerField(required=False)

class ArtykulViewSerializer(serializers.Serializer):
    artykul_id = serializers.IntegerField(read_only=True)
    tresc = serializers.CharField(required=True,allow_blank=False)
    nazwa_kursu = serializers.CharField(max_length=50,required=True)
    id = serializers.IntegerField()

class PytanieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tresc = serializers.CharField(required=True,allow_blank=False)

class OdpowiedzSerializer(serializers.Serializer):
    text = serializers.CharField(allow_blank=False)
    correct = serializers.BooleanField(required=True)

class RozdzialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nazwa_rozdzialu = serializers.CharField()
    kurs_id = serializers.IntegerField()

class PytaniaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tresc = serializers.CharField()
    artykul_id = serializers.IntegerField()

class OdpowiedziSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tresc = serializers.CharField(allow_blank=False)
    poprawna = serializers.BooleanField(required=True)
    pytanie_id = serializers.IntegerField()