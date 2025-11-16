from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import connection
from .serializers import UserSerializer,UserSerializerWithToken
import random
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import KursSerializer,ArtykulSerializer,PytanieSerializer,QuizSerializer,SprawdzOdpowiedzSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework.views import APIView

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user

    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    except:
        message = {'error':'taka osoba juz istnieje'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)

class Kursy(APIView):
    """GET - lista kursów
       POST - dodanie kursu tylko dla admina
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nazwa_kursu FROM kursy_kurs;")
            rows = cursor.fetchall()

        if not rows:
            return Response({"error": "Brak kursów"}, status=status.HTTP_404_NOT_FOUND)

        kursy = [{"id": r[0], "nazwa_kursu": r[1]} for r in rows]
        serializer = KursSerializer(kursy, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KursSerializer(data=request.data)
        if serializer.is_valid():
            nazwa_kursu = serializer.validated_data["nazwa_kursu"]

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO kursy_kurs (nazwa_kursu) VALUES (%s) RETURNING id;",
                    [nazwa_kursu]
                )
                new_id = cursor.fetchone()[0]

            kurs = {"id": new_id, "nazwa_kursu": nazwa_kursu}
            return Response(KursSerializer(kurs).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Kurs(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM kursy_kurs WHERE id=%s;", [id])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Nie znaleziono kursu"}, status=status.HTTP_404_NOT_FOUND)

        kurs = {"id": row[0], "nazwa_kursu": row[1]}
        return Response(KursSerializer(kurs).data, status=status.HTTP_200_OK)


class Artykuly(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nazwa_kursu):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM artykul_kurs_view WHERE nazwa_kursu=%s;",
                [nazwa_kursu]
            )
            rows = cursor.fetchall()

        if not rows:
            return Response(
                {"error": f"Brak artykułów dla kursu '{nazwa_kursu}'"},
                status=status.HTTP_404_NOT_FOUND
            )

        artykuly = [
            {"id": r[0], "tresc": r[1], "nazwa_kursu": r[2], "id_kursu": r[3]}
            for r in rows
        ]

        return Response(ArtykulSerializer(artykuly, many=True).data)


class Artykul(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM artykul_kurs_view WHERE artykul_id=%s;",
                [id]
            )
            row = cursor.fetchone()

        if not row:
            return Response(
                {"error": f"Nie znaleziono artykułu o id: {id}"},
                status=status.HTTP_404_NOT_FOUND
            )

        artykul = {
            "id": row[0],
            "tresc": row[1],
            "nazwa_kursu": row[2],
            "id_kursu": row[3]
        }

        return Response(ArtykulSerializer(artykul).data)


class Start_quiz(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        kursy_param = request.GET.get("kursy")
        count = int(request.GET.get("liczba_pytan", 20))

        if not kursy_param or count <= 0:
            return Response({"error": "Podaj poprawne dane"}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.tresc
                FROM kursy_pytanie p
                JOIN artykul_kurs_view ak ON ak.artykul_id = p.artykul_id
                WHERE ak.nazwa_kursu = %s
            """, [kursy_param])
            rows = cursor.fetchall()

        if count < len(rows):
            rows = random.sample(rows, count)

        quiz = []

        for row in rows:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT o.tresc, o.poprawna
                    FROM kursy_odpowiedz o
                    WHERE pytanie_id=%s;
                """, [row[0]])
                odpowiedzi = cursor.fetchall()

            quiz.append({
                "id": row[0],
                "tresc": row[1],
                "odpowiedzi": [{"text": o[0], "correct": o[1]} for o in odpowiedzi]
            })

        return Response(QuizSerializer(quiz, many=True).data)


class Sprawdz_quiz(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SprawdzOdpowiedzSerializer(
            request.data.get("odpowiedzi"),
            many=True
        )

        if not serializer.is_valid():
            return Response(
                {"error": "Zły format odpowiedzi"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT tresc, pytanie_id FROM kursy_odpowiedz WHERE poprawna=true;"
            )
            poprawne_odpowiedzi = cursor.fetchall()

        wynik = 0
        poprawne_id = []

        for odp in serializer.validated_data:
            pyt_id = odp["pytanie_id"]
            wybrana = odp["wybrana_opcja"]

            if (wybrana, pyt_id) in poprawne_odpowiedzi:
                wynik += 1
                poprawne_id.append(pyt_id)

        return Response({
            "punkty": wynik,
            "poprawne": poprawne_id
        })


"""
TODO 
Artykul POST/PUT/DELETE
KURS PUT/DELETE
ROZDZIAL GET/POST/PUT/DELETE
PYTANIA GET/POST/PUT/DELETE
ODPOWIEDZ GET/POST/PUT/DELETE
ZAPISARTYKULU GET/DELETE/POST
NOTATKA GET/POST/PUT/DELETE
KOMENTARZ GET/POST/PUT/DELETE
STATYSTYKIPYTANIA GET/PUT/PATCH?
PROGRESSPYTAN GET/PUT/PATCH
WYNIKIEGZAMINU POST/GET/PUT/PATCH
OCENAARTYKULU GET/POST/PATCH/PUT?
"""