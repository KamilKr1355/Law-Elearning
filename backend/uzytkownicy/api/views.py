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
@permission_classes([AllowAny])
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
        
        if User.objects.filter(username=validated_data['username']).exists():
            return Response({'error': 'Użytkownik o tej nazwie już istnieje.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=validated_data['email']).exists():
            return Response({'error': 'Ten email jest już zajęty.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(
                username = validated_data['username'],
                email = validated_data['email'],
                first_name = validated_data.get('name', ''),
                password = make_password(validated_data['password']) 
            )

            token_serializer = UserSerializerWithToken(user, many=False)
            return Response(token_serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"BŁĄD REJESTRACJI: {str(e)}") 
            return Response({'error': f'Błąd serwera: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='put',
    operation_description="ADMIN: Nadaje uprawnienia administratora (staff) wybranemu użytkownikowi.",
    responses={
        status.HTTP_200_OK: "Użytkownik został administratorem.",
        status.HTTP_404_NOT_FOUND: "Nie znaleziono użytkownika.",
        status.HTTP_403_FORBIDDEN: "Tylko administrator może wykonać tę akcję."
    }
)
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def promoteToAdmin(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.is_staff = True
        user.save()
        return Response({'message': f'Użytkownik {user.username} został administratorem.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Użytkownik nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    operation_description="ADMIN: Banuje użytkownika (ustawia is_active=False) lub go odblokowuje.",
    responses={
        status.HTTP_200_OK: "Status użytkownika został zmieniony.",
        status.HTTP_404_NOT_FOUND: "Nie znaleziono użytkownika."
    }
)
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def toggleUserBan(request, pk):
    try:
        user = User.objects.get(id=pk)
        
        # Zabezpieczenie przed banowaniem samego siebie
        if user == request.user:
            return Response({'error': 'Nie możesz zbanować samego siebie.'}, status=status.HTTP_400_BAD_REQUEST)

        # Przełączamy status is_active
        user.is_active = not user.is_active
        user.save()
        
        status_msg = "aktywny" if user.is_active else "zbanowany"
        return Response({'message': f'Użytkownik {user.username} jest teraz {status_msg}.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Użytkownik nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='delete',
    operation_description="ADMIN: Całkowite usunięcie użytkownika z bazy danych.",
    responses={
        status.HTTP_200_OK: "Użytkownik usunięty.",
        status.HTTP_404_NOT_FOUND: "Nie znaleziono użytkownika."
    }
)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return Response({'message': 'Użytkownik został usunięty.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Użytkownik nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)