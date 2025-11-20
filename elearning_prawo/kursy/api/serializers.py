from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens  import RefreshToken # type: ignore
from django.contrib.auth.models import User
from kursy.models import Kurs



class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    isAdmin = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ['id','username','email','name','isAdmin']


    def get_isAdmin(self,obj):
        return obj.is_staff

    def get_name(self,obj):
        name = obj.first_name

        if name == "":
            name = obj.email
        return name
    
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ['id','username','email','name','isAdmin','token']

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
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

class RozdzialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nazwa_rozdzialu = serializers.CharField()
    kurs_id = serializers.IntegerField()