from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView 
from .serializers import UserSerializer,UserSerializerWithToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
from .serializers import RegisterUserInputSerializer

user_schema = openapi.Response("Obiekt Użytkownika.", UserSerializer)
user_list_schema = openapi.Response("Lista Użytkowników.", UserSerializer(many=True))
user_with_token_schema = openapi.Response("Obiekt Użytkownika z Tokenem JWT.", UserSerializerWithToken)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        
        serializer = UserSerializerWithToken(self.user).data

        for k,v in serializer.items():
            data[k] = v

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['message'] = 'hello world'
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@swagger_auto_schema(
    method='get',
    operation_description="POBIERANIE: Zwraca szczegółowe dane profilowe zalogowanego użytkownika.",
    responses={
        status.HTTP_200_OK: user_schema,
        status.HTTP_401_UNAUTHORIZED: "Wymagana autoryzacja (JWT Token)."
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user

    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    operation_description="POBIERANIE: Zwraca listę wszystkich użytkowników w systemie. Dostępne tylko dla administratorów.",
    responses={
        status.HTTP_200_OK: user_list_schema,
        status.HTTP_403_FORBIDDEN: "Wymagane uprawnienia administratora."
    }
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="REJESTRACJA: Tworzy nowe konto użytkownika. Zwraca od razu token JWT do zalogowania.",
    request_body=RegisterUserInputSerializer,
    responses={
        status.HTTP_200_OK: user_with_token_schema, 
        status.HTTP_400_BAD_REQUEST: "Błąd walidacji danych wejściowych lub użytkownik już istnieje."
    }
)
@api_view(['POST'])
def registerUser(request):
    serializer = RegisterUserInputSerializer(data=request.data)
    
    if serializer.is_valid():
        validated_data = serializer.validated_data 
        
        try:
            user = User.objects.create(
                username = validated_data['username'],
                email = validated_data['email'],
                password = make_password(validated_data['password']) 
            )

            token_serializer = UserSerializerWithToken(user, many=False)
            return Response(token_serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            message = {'error': 'Taka osoba już istnieje.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)