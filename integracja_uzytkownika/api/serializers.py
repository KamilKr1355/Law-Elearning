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
    wybrana_opcja = serializers.CharField()