from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens  import RefreshToken 
from django.contrib.auth.models import User
from kursy.models import Kurs

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    isAdmin = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ['id','username','email','name','isAdmin','is_active']


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
        fields = ['id','username','email','name','isAdmin','is_active','token']

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
class RegisterUserInputSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8 
    )